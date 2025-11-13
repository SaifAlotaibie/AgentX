import { useState, useRef, useCallback, useEffect } from 'react';
import { useMicVAD } from '@ricky0123/vad-react';
import { MOCK_USER } from '../config/mockUser';

const API_BASE_URL = 'http://localhost:8000';
const MAX_RECORDING_TIME = 90000; // 90 seconds per turn
const AUTO_STOP_TIME = 30000; // 30 seconds auto-stop

/**
 * Hook for managing continuous voice call sessions.
 * Implements a loop: listen → transcribe → send → receive response → play audio → listen again
 */
export const useVoiceCall = () => {
  const [isInCall, setIsInCall] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentMessage, setCurrentMessage] = useState('');
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recordingTimeoutRef = useRef(null);
  const streamRef = useRef(null);
  const audioPlayerRef = useRef(null);
  const shouldContinueRef = useRef(false); // Controls the conversation loop
  const websocketRef = useRef(null);
  const sessionIdRef = useRef(null); // Store sessionId for use in callbacks
  const userIdRef = useRef(MOCK_USER.id); // Consistent userId across sessions

  // Voice Activity Detection (disabled for now - using manual stop)
  const vad = useMicVAD({
    startOnLoad: false,
    onSpeechStart: () => {
      console.log('[Call] 🗣️ Speech STARTED (VAD)');
    },
    onSpeechEnd: async () => {
      if (shouldContinueRef.current && mediaRecorderRef.current) {
        console.log('[Call] 🛑 Speech ENDED (VAD) - auto-stopping...');
        await stopListening();
      }
    },
    redemptionFrames: 25, // ~800ms of silence before ending
    positiveSpeechThreshold: 0.5,
  });

  // Start listening for user speech
  const startListening = useCallback(async () => {
    console.log('[Call] 📞 startListening() called!');
    console.log('[Call] isInCall:', isInCall, 'isListening:', isListening);
    console.log('[Call] shouldContinueRef.current:', shouldContinueRef.current);
    
    if (!shouldContinueRef.current) {
      console.log('[Call] ❌ shouldContinue is false, not starting');
      return;
    }
    
    if (isListening) {
      console.log('[Call] ⚠️ Already listening, skipping');
      return;
    }

    try {
      setError(null);
      audioChunksRef.current = [];
      
      console.log('[Call] 🎤 Requesting microphone access...');

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
        }
      });
      console.log('[Call] ✅ Microphone access GRANTED!');

      streamRef.current = stream;

      // Start VAD to detect when user stops speaking
      try {
        console.log('[Call] 🎯 Starting VAD (Voice Activity Detection)...');
        vad.start();
        console.log('[Call] ✅ VAD is active - will auto-stop when you finish speaking!');
      } catch (vadError) {
        console.warn('[Call] ⚠️ VAD failed, falling back to 30s timeout:', vadError);
      }

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      const mediaRecorder = new MediaRecorder(stream, { mimeType });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      console.log('[Call] 🎤 Starting MediaRecorder...');
      mediaRecorder.start(100);
      mediaRecorderRef.current = mediaRecorder;
      setIsListening(true);
      setCurrentMessage('🎤 جاري الاستماع... تحدث الآن!'); // Clear previous message
      console.log('[Call] ✅✅✅ RECORDING IS ACTIVE! User can speak now!');

      recordingTimeoutRef.current = setTimeout(() => {
        console.log('[Call] ⏰ Max recording time reached (30s)');
        stopListening();
      }, MAX_RECORDING_TIME);

    } catch (err) {
      console.error('[Call] ❌ ERROR starting to listen:', err);
      console.error('[Call] Error name:', err.name);
      console.error('[Call] Error message:', err.message);
      setError('فشل الوصول إلى الميكروفون: ' + err.message);
    }
  }, []); // No dependencies - use refs!

  // Stop listening and process speech
  const stopListening = useCallback(async () => {
    if (!mediaRecorderRef.current) {
      console.log('[Call] ⚠️ No media recorder active');
      return;
    }
    
    if (!isListening) {
      console.log('[Call] ⚠️ Not currently listening');
      return;
    }

    console.log('[Call] 🛑 Stopping listening and processing audio...');

    return new Promise((resolve) => {
      const mediaRecorder = mediaRecorderRef.current;

      mediaRecorder.onstop = async () => {
        // Pause VAD
        try {
          vad.pause();
          console.log('[Call] ✅ VAD paused');
        } catch (e) {
          console.warn('[Call] ⚠️ VAD pause error:', e);
        }

        if (recordingTimeoutRef.current) {
          clearTimeout(recordingTimeoutRef.current);
        }

        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
          streamRef.current = null;
        }

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        console.log(`[Call] Audio blob size: ${audioBlob.size} bytes`);

        setIsListening(false);
        setIsProcessing(true);

        // Check for end call command before transcription
        try {
          console.log('[Call] Transcribing...');
          const formData = new FormData();
          formData.append('audio', audioBlob, 'recording.webm');

          const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (data.success && data.text) {
            const transcript = data.text.trim();
            console.log('[Call] Transcript:', transcript);

            // Check for end call commands
            const endCallPhrases = [
              'أغلق المكالمة',
              'انهي المكالمة',
              'إنهاء المكالمة',
              'شكرا وداعا',
              'مع السلامة',
              'close call',
              'end call',
              'goodbye'
            ];

            const shouldEndCall = endCallPhrases.some(phrase => 
              transcript.toLowerCase().includes(phrase.toLowerCase())
            );

            if (shouldEndCall) {
              console.log('[Call] End call command detected');
              endCall();
              resolve();
              return;
            }

            // Send to agent
            await sendToAgent(transcript);
          } else {
            setError('فشل تحويل الصوت إلى نص');
          }
        } catch (err) {
          console.error('[Call] Processing error:', err);
          setError('خطأ في المعالجة');
          // Continue the loop even on error
          if (shouldContinueRef.current) {
            setTimeout(() => startListening(), 1000);
          }
        } finally {
          setIsProcessing(false);
        }

        resolve();
      };

      mediaRecorder.stop();
    });
  }, [isListening]); // vad removed

  // Send message to agent via WebSocket
  const sendToAgent = useCallback(async (text) => {
    if (!websocketRef.current || websocketRef.current.readyState !== WebSocket.OPEN) {
      setError('لا يوجد اتصال بالوكيل');
      return;
    }

    console.log('[Call] Sending to agent:', text);
    setCurrentMessage('جاري التفكير...');

    // Send message (use consistent userId from refs)
    websocketRef.current.send(JSON.stringify({
      type: 'user_message',
      message: text,
      sessionId: sessionIdRef.current || `CALL_${Date.now()}`,
      userId: userIdRef.current || MOCK_USER.id,
      userRole: 'employee'
    }));

    // Response will be handled by WebSocket onmessage
  }, []);

  // Play audio response
  const playAudioResponse = useCallback(async (audioUrl) => {
    return new Promise((resolve, reject) => {
      console.log('[Call] Playing audio:', audioUrl);
      setIsSpeaking(true);

      const audio = new Audio(audioUrl);
      audioPlayerRef.current = audio;

      audio.onplay = () => {
        console.log('[Call] Audio playback started');
      };

      audio.onended = () => {
        console.log('[Call] Audio playback ended');
        setIsSpeaking(false);
        audioPlayerRef.current = null;
        resolve();
      };

      audio.onerror = (e) => {
        console.error('[Call] Audio playback error:', e);
        setIsSpeaking(false);
        reject(e);
      };

      audio.play().catch(reject);
    });
  }, []);

  // Start the call
  const startCall = useCallback(async () => {
    console.log('🚀 [Call] Starting call...');
    console.log('🚀 [Call] Setting isInCall to true');
    setIsInCall(true);
    shouldContinueRef.current = true;
    setError(null);
    setCurrentMessage('مرحباً! كيف يمكنني مساعدتك؟');

    // Use consistent userId across all sessions
    const userId = MOCK_USER.id; // Use mock user ID
    const sessionId = `CALL_${Date.now()}`;
    
    // Store in refs for use in callbacks
    sessionIdRef.current = sessionId;
    userIdRef.current = userId;
    
    console.log(`[Call] Using userId: ${userId}, sessionId: ${sessionId}`);

    // Connect WebSocket
    const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}/${userId}/employee`);
    
    ws.onopen = () => {
      console.log('[Call] ✅ WebSocket connected');
      websocketRef.current = ws;
      
      // Start listening after a brief welcome
      console.log('[Call] Will start listening in 2 seconds...');
      setTimeout(() => {
        console.log('[Call] 2 seconds passed, calling startListening()...');
        startListening();
      }, 2000);
    };

    ws.onmessage = async (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('[Call] Received:', data.type);

        if (data.type === 'chat_message' && data.role === 'assistant') {
          setCurrentMessage(data.message);
        } else if (data.type === 'audio_response') {
          setCurrentMessage(data.text);
          
          // Auto-play the response
          try {
            await playAudioResponse(`${API_BASE_URL}${data.audioUrl}`);
            
            // Continue listening if call is still active (use ref, not state!)
            if (shouldContinueRef.current) {
              console.log('[Call] Resuming listening...');
              setTimeout(() => {
                startListening();
              }, 500);
            }
          } catch (err) {
            console.error('[Call] Audio play error:', err);
            // Continue anyway
            if (shouldContinueRef.current) {
              setTimeout(() => startListening(), 1000);
            }
          }
        }
      } catch (err) {
        console.error('[Call] Message parse error:', err);
      }
    };

    ws.onerror = (error) => {
      console.error('[Call] WebSocket error:', error);
      setError('خطأ في الاتصال');
    };

    ws.onclose = () => {
      console.log('[Call] WebSocket closed');
      websocketRef.current = null;
    };

  }, [startListening, playAudioResponse]); // Removed isInCall from dependencies

  // End the call
  const endCall = useCallback(() => {
    console.log('[Call] Ending call...');
    shouldContinueRef.current = false;
    setIsInCall(false);
    setIsListening(false);
    setIsSpeaking(false);
    setIsProcessing(false);
    setCurrentMessage('');

    // Stop any active recording
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }

    // Stop stream
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    // Stop audio
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      audioPlayerRef.current = null;
    }

    // Stop VAD
    try {
      vad.pause();
      console.log('[Call] VAD stopped');
    } catch (e) {
      console.warn('[Call] VAD stop error:', e);
    }

    // Close WebSocket
    if (websocketRef.current) {
      websocketRef.current.close();
      websocketRef.current = null;
    }

    // Clear timeouts
    if (recordingTimeoutRef.current) {
      clearTimeout(recordingTimeoutRef.current);
    }
  }, []); // vad removed since it's disabled

  // Auto-stop recording after 30 seconds (since VAD is disabled)
  useEffect(() => {
    if (isListening && isInCall) {
      const autoStopTimeout = setTimeout(() => {
        console.log('[Call] Auto-stopping after 30 seconds');
        stopListening();
      }, AUTO_STOP_TIME);
      
      return () => clearTimeout(autoStopTimeout);
    }
  }, [isListening, isInCall, stopListening]);

  // Cleanup on unmount (no dependencies to avoid React Strict Mode double-invoke)
  useEffect(() => {
    return () => {
      // Only cleanup if actually in a call
      if (shouldContinueRef.current || mediaRecorderRef.current || websocketRef.current) {
        console.log('[Call] Cleanup on unmount');
        endCall();
      }
    };
  }, [endCall]);

  return {
    isInCall,
    isListening,
    isSpeaking,
    isProcessing,
    currentMessage,
    error,
    startCall,
    endCall,
    stopListening,  // NEW: Export stopListening so user can manually stop
  };
};


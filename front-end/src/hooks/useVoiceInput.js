import { useState, useRef, useCallback } from 'react';
import { useMicVAD } from '@ricky0123/vad-react';

const MAX_RECORDING_TIME = 90000; // 90 seconds
const API_BASE_URL = 'http://localhost:8000';

export const useVoiceInput = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recordingTimeoutRef = useRef(null);
  const streamRef = useRef(null);
  
  // Voice Activity Detection
  const vad = useMicVAD({
    startOnLoad: false,
    onSpeechEnd: async (audio) => {
      // Auto-stop after silence detected
      if (isRecording) {
        console.log('[VAD] Silence detected, stopping recording');
        await stopRecording();
      }
    },
    redemptionFrames: 30, // Wait ~1 second of silence before stopping
    positiveSpeechThreshold: 0.6,
  });

  const startRecording = async () => {
    try {
      setError(null);
      setTranscript('');
      audioChunksRef.current = [];
      
      console.log('[Voice] Starting recording...');
      
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000, // Whisper prefers 16kHz
          echoCancellation: true,
          noiseSuppression: true,
        } 
      });
      
      streamRef.current = stream;
      
      // Start VAD
      try {
        vad.start();
        console.log('[VAD] Started');
      } catch (vadError) {
        console.warn('[VAD] Failed to start, continuing without VAD:', vadError);
      }
      
      // Setup MediaRecorder
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstart = () => {
        console.log('[MediaRecorder] Started');
      };
      
      mediaRecorder.start(100); // Collect data every 100ms
      mediaRecorderRef.current = mediaRecorder;
      setIsRecording(true);
      
      // Auto-stop after 90 seconds
      recordingTimeoutRef.current = setTimeout(() => {
        console.log('[Voice] Max recording time reached');
        stopRecording();
      }, MAX_RECORDING_TIME);
      
    } catch (err) {
      console.error('[Voice] Error starting recording:', err);
      setError('فشل الوصول إلى الميكروفون');
      setIsRecording(false);
    }
  };

  const stopRecording = useCallback(async () => {
    if (!mediaRecorderRef.current || !isRecording) {
      console.log('[Voice] Stop called but not recording');
      return;
    }
    
    console.log('[Voice] Stopping recording...');
    
    return new Promise((resolve) => {
      const mediaRecorder = mediaRecorderRef.current;
      
      mediaRecorder.onstop = async () => {
        console.log('[MediaRecorder] Stopped');
        
        // Stop VAD
        try {
          vad.pause();
          console.log('[VAD] Paused');
        } catch (e) {
          console.warn('[VAD] Error pausing:', e);
        }
        
        // Clear timeout
        if (recordingTimeoutRef.current) {
          clearTimeout(recordingTimeoutRef.current);
          recordingTimeoutRef.current = null;
        }
        
        // Stop all tracks
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => {
            track.stop();
            console.log('[Stream] Track stopped');
          });
          streamRef.current = null;
        }
        
        // Create audio blob
        const audioBlob = new Blob(audioChunksRef.current, { 
          type: 'audio/webm' 
        });
        
        console.log(`[Voice] Audio blob size: ${audioBlob.size} bytes`);
        
        setIsRecording(false);
        setIsProcessing(true);
        
        // Send to backend for transcription
        try {
          console.log('[Whisper] Sending audio for transcription...');
          
          const formData = new FormData();
          formData.append('audio', audioBlob, 'recording.webm');
          
          const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
            method: 'POST',
            body: formData,
          });
          
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          const data = await response.json();
          
          console.log('[Whisper] Transcription result:', data);
          
          if (data.success && data.text) {
            setTranscript(data.text);
            console.log('[Voice] ✓ Transcription successful');
          } else {
            setError('فشل تحويل الصوت إلى نص');
            console.error('[Voice] Transcription failed: no text in response');
          }
        } catch (err) {
          console.error('[Voice] Transcription error:', err);
          setError('فشل الاتصال بالخادم');
        } finally {
          setIsProcessing(false);
        }
        
        resolve();
      };
      
      mediaRecorder.stop();
    });
  }, [isRecording, vad]);
  
  const resetTranscript = () => {
    setTranscript('');
    setError(null);
  };
  
  return {
    isListening: isRecording,
    isProcessing,
    transcript,
    error,
    startListening: startRecording,
    stopListening: stopRecording,
    resetTranscript,
  };
};

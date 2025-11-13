# 🎙️ Voice Integration Guide - AgentX

**Status**: ✅ Fully Implemented  
**Date**: November 12, 2025  
**Features**: Speech-to-Text (Whisper) + Text-to-Speech (OpenAI TTS) in Arabic

---

## 🎯 Overview

The system now supports **full voice interaction** for a hands-free, natural conversation experience with the Qiwa AI Agent.

### User Flow
```
1. User clicks microphone button 🎤
2. Speaks in Arabic (or any language)
3. System auto-detects silence OR user clicks mic again
4. Audio transcribed via Whisper → text appears in input
5. User sends message
6. Agent processes and responds with text + audio
7. User can play audio response by clicking speaker icon 🔊
```

---

## 🔧 Technical Architecture

### Backend (Python + FastAPI)

#### 1. Speech-to-Text Endpoint
**File**: `backend/Agents/app.py`

```python
@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile):
    # Receives audio (webm/mp3/wav)
    # Calls OpenAI Whisper API
    # Returns: {"text": "transcribed text", "language": "ar", "success": true}
```

**Technology**: OpenAI Whisper API  
**Cost**: $0.006/minute  
**Language**: Arabic (ar)  
**Max Duration**: 90 seconds

#### 2. Text-to-Speech Generation
**File**: `backend/Agents/routers/real_employee_router.py`

```python
# After agent generates text response
openai_client.audio.speech.create(
    model="tts-1",
    voice="alloy",  # Neutral voice, excellent for Arabic
    input=response,
    response_format="mp3"
)
```

**Technology**: OpenAI TTS API  
**Cost**: $15/1M characters (~$0.001 per response)  
**Voice**: "alloy" (neutral, clear for Arabic)  
**Format**: MP3

#### 3. Audio File Serving
**File**: `backend/Agents/app.py`

```python
@app.get("/api/audio/{filename}")
async def serve_audio(filename: str):
    # Serves MP3 files from logs/audio/
    return FileResponse(audio_path, media_type="audio/mpeg")
```

**Storage**: `backend/Agents/logs/audio/*.mp3`  
**Lifetime**: Persistent (not auto-deleted)

---

### Frontend (React + Vite)

#### 1. Voice Input Hook
**File**: `front-end/src/hooks/useVoiceInput.js`

**Features**:
- MediaRecorder API for high-quality audio capture
- Voice Activity Detection (VAD) using `@ricky0123/vad-react`
- 90-second max recording with timeout
- Auto-stop on silence detection
- Manual stop (click mic again)
- Real-time processing feedback

**States**:
- `isListening`: Recording in progress
- `isProcessing`: Uploading/transcribing
- `transcript`: Transcribed text
- `error`: Error messages

**Functions**:
- `startListening()`: Begin recording
- `stopListening()`: Stop and transcribe
- `resetTranscript()`: Clear transcript

#### 2. Audio Player Hook
**File**: `front-end/src/hooks/useAudioPlayer.js`

**Features**:
- Play/pause TTS audio responses
- Track currently playing audio
- Auto-cleanup on finish
- Error handling

**States**:
- `isPlaying`: Playback status
- `currentAudio`: URL of playing audio

**Functions**:
- `playAudio(url)`: Play audio
- `stopAudio()`: Stop playback
- `toggleAudio(url)`: Toggle play/pause

#### 3. UI Components

**InputBar** (`components/chat/InputBar.jsx`):
- Microphone button with state indicators:
  - 🎤 Gray: Ready
  - 🔴 Red (pulsing): Recording
  - 🟡 Yellow: Processing
  - ❌ Disabled: During transcription
- Dynamic placeholder text showing current state

**MessageBubble** (`components/chat/MessageBubble.jsx`):
- Speaker icon button on assistant messages with audio
- Visual feedback: 🔊 (play) / 🔇 (stop)
- Text: "استماع للرد" / "إيقاف الصوت"

---

## 📊 Data Flow

### Voice Input (STT)
```
User Speech
    ↓
MediaRecorder (WebM audio)
    ↓
VAD detects silence OR user clicks stop
    ↓
FormData upload to /api/transcribe
    ↓
Whisper API transcription
    ↓
Text returned to frontend
    ↓
Displayed in input box
```

### Voice Output (TTS)
```
Agent generates text response
    ↓
Router calls OpenAI TTS API
    ↓
MP3 file saved to logs/audio/
    ↓
WebSocket event: audio_response
    {
      "type": "audio_response",
      "audioUrl": "/api/audio/tts_S123_1234567890.mp3",
      "text": "agent response",
      "timestamp": "..."
    }
    ↓
Frontend adds message with audioUrl
    ↓
Audio player button rendered
    ↓
User clicks to play
```

---

## 🧪 Testing Guide

### Prerequisites
1. OpenAI API key configured ✓
2. Backend running on port 8000
3. Frontend running on port 5173
4. Microphone permissions granted in browser

### Test 1: Basic Voice Input
1. Navigate to chat page
2. Click microphone button (should turn red and pulse)
3. Speak: "مرحباً"
4. Wait ~1 second (VAD should auto-stop)
5. Verify text "مرحباً" appears in input box
6. Click send

**Expected**: Transcription successful, message sent

### Test 2: Manual Stop
1. Click microphone
2. Speak: "أريد إضافة سيرتي الذاتية"
3. Click microphone again immediately (before VAD stops)
4. Verify text appears

**Expected**: Recording stops, transcription completes

### Test 3: 90-Second Timeout
1. Click microphone
2. Let it record for 90 seconds without speaking
3. Verify auto-stop at 90 seconds

**Expected**: "Max recording time reached" in console, recording stops

### Test 4: TTS Playback
1. Send any message (voice or text)
2. Wait for agent response
3. Look for speaker icon (🔊) below assistant message
4. Click "استماع للرد"
5. Verify audio plays in Arabic
6. Click "إيقاف الصوت" to stop

**Expected**: Audio plays, stops on command

### Test 5: Full Voice Conversation
1. **Voice**: "أريد إضافة سيرتي الذاتية"
2. **Agent** (with audio): "ما هو اسمك الكامل؟"
3. Click audio to hear response
4. **Voice**: "اسمي أحمد محمد العتيبي"
5. **Agent** (with audio): "ما هو المسمى الوظيفي؟"
6. **Voice**: "مهندس برمجيات"
7. Continue until resume created

**Expected**: Smooth voice-only conversation flow

### Test 6: Mixed Input (Voice + Text)
1. Use voice for one message
2. Use text for next message
3. Use voice again

**Expected**: Both methods work seamlessly

### Test 7: Error Handling
1. Block microphone permissions
2. Click microphone
3. Verify error message: "فشل الوصول إلى الميكروفون"

**Expected**: Graceful error, no crash

### Test 8: Multiple Audio Playback
1. Have 3+ agent responses with audio
2. Play first audio
3. Before it finishes, play second audio
4. Verify first stops, second plays

**Expected**: Only one audio plays at a time

---

## 🔧 Configuration

### Adjusting Recording Duration
**File**: `front-end/src/hooks/useVoiceInput.js`

```javascript
const MAX_RECORDING_TIME = 90000; // 90 seconds (in milliseconds)
```

Change to any value (in ms):
- 60000 = 1 minute
- 120000 = 2 minutes

### Changing TTS Voice
**File**: `backend/Agents/routers/real_employee_router.py`

```python
audio_response = openai_client.audio.speech.create(
    voice="alloy",  # Change this
)
```

Available voices:
- `alloy` (neutral, recommended for Arabic)
- `echo` (male)
- `fable` (British accent)
- `onyx` (deep male)
- `nova` (warm female)
- `shimmer` (soft female)

### VAD Sensitivity
**File**: `front-end/src/hooks/useVoiceInput.js`

```javascript
const vad = useMicVAD({
    redemptionFrames: 30, // Wait frames (~1 second)
    positiveSpeechThreshold: 0.6, // Sensitivity (0-1)
});
```

Adjustments:
- **More sensitive** (stops faster): Decrease `redemptionFrames` to 20
- **Less sensitive** (waits longer): Increase to 45
- **Quieter environments**: Decrease `positiveSpeechThreshold` to 0.4

---

## 📈 Performance Metrics

### Latency Breakdown
| Stage | Duration |
|-------|----------|
| Recording | 2-5 seconds (user-dependent) |
| VAD detection | ~1 second after speech ends |
| Upload to backend | 0.5-1 second |
| Whisper transcription | 2-4 seconds |
| **Total STT** | **5-11 seconds** |
| Agent LLM processing | 2-5 seconds |
| TTS generation | 1-2 seconds |
| **Total Response** | **3-7 seconds** |

**Full interaction** (voice → audio response): ~8-18 seconds

### Cost Per Interaction
| Service | Usage | Cost |
|---------|-------|------|
| Whisper STT | ~30 seconds audio | $0.003 |
| GPT-4o-mini | 1 request (~500 tokens) | $0.0001 |
| TTS | ~100 characters | $0.0015 |
| **Total** | Per voice interaction | **~$0.005** |

**100 conversations/day** = $0.50/day = $15/month

---

## 🐛 Troubleshooting

### Issue 1: "Microphone access denied"
**Symptoms**: Red microphone icon, error message  
**Cause**: Browser permissions not granted  
**Solution**:
1. Click lock icon in browser address bar
2. Allow microphone access
3. Refresh page

### Issue 2: "VAD not working, recording doesn't stop"
**Symptoms**: Recording continues forever  
**Cause**: VAD library failed to initialize  
**Solution**: Manual stop works (click mic again). Check console for VAD errors.

### Issue 3: "Transcription fails with 500 error"
**Symptoms**: Processing indicator, then error  
**Cause**: OpenAI API issue or invalid audio format  
**Solution**:
1. Check backend logs for error details
2. Verify `OPENAI_API_KEY` is correct
3. Ensure audio file is valid (check temp file size)

### Issue 4: "Audio doesn't play"
**Symptoms**: Speaker icon present, but no sound  
**Cause**: TTS file not generated or CORS issue  
**Solution**:
1. Check `backend/Agents/logs/audio/` for MP3 files
2. Open browser DevTools → Network → Check `/api/audio/...` request
3. Verify backend console for "✓ TTS audio generated" message

### Issue 5: "Text appears in wrong language"
**Symptoms**: English transcription instead of Arabic  
**Cause**: Whisper auto-detected wrong language  
**Solution**: Audio was likely in English. Speak clearly in Arabic.

### Issue 6: "Excessive API costs"
**Symptoms**: High OpenAI bills  
**Cause**: Many long recordings  
**Solution**:
1. Reduce `MAX_RECORDING_TIME` to 30-60 seconds
2. Implement rate limiting (max 10 recordings/minute per user)
3. Consider caching common responses

---

## 📚 Code Reference

### Key Files

**Backend**:
- `backend/Agents/app.py` - Whisper & audio serving endpoints
- `backend/Agents/routers/real_employee_router.py` - TTS generation
- `backend/Agents/config/settings.py` - Configuration

**Frontend**:
- `front-end/src/hooks/useVoiceInput.js` - Voice input logic
- `front-end/src/hooks/useAudioPlayer.js` - Audio playback
- `front-end/src/components/chat/InputBar.jsx` - Mic button UI
- `front-end/src/components/chat/MessageBubble.jsx` - Audio player UI
- `front-end/src/hooks/useWebSocket.js` - WebSocket handling
- `front-end/src/store/chatStore.js` - State management

### Dependencies

**Backend** (Python):
- `openai>=1.3.0` - Whisper & TTS APIs
- `fastapi>=0.104.0` - Web framework
- `python-multipart` - File uploads (auto-installed)

**Frontend** (npm):
- `@ricky0123/vad-react@^2.0.0` - Voice Activity Detection
- React, Vite (existing)

---

## 🚀 Future Enhancements

### Possible Improvements
1. **Real-time Streaming**: Stream audio as agent speaks (lower latency)
2. **Voice Profiles**: Remember user's voice for personalization
3. **Noise Cancellation**: Better audio processing before transcription
4. **Offline Mode**: Download TTS responses for offline playback
5. **Multi-language**: Automatic language detection beyond Arabic
6. **Voice Commands**: "Stop", "Repeat", "Louder" without typing

### Advanced Features
- **Conversation History Audio**: Playback entire conversation
- **Voice Shortcuts**: "Open dashboard", "Close ticket" by voice
- **Accessibility**: Fully voice-navigable UI for visually impaired users
- **Mobile App**: Native audio recording for better quality

---

## ✅ Summary

Voice integration is **fully functional** with:
- ✅ OpenAI Whisper (STT) with Arabic support
- ✅ OpenAI TTS (alloy voice) for responses
- ✅ Voice Activity Detection (auto-stop)
- ✅ 90-second max recording with timeout
- ✅ Manual stop via button click
- ✅ Audio playback controls in chat
- ✅ Real-time processing indicators
- ✅ Error handling and fallbacks
- ✅ Cost-effective (~$0.005 per interaction)
- ✅ Non-breaking (text chat still works)

**Cost**: $0.02 per full voice conversation (including agent processing)  
**Latency**: 8-18 seconds end-to-end  
**Languages**: Arabic (primary), multi-language support via Whisper  

The system is ready for production use! 🎉


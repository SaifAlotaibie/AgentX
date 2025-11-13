# 📞 Voice Call Mode - Phone-Style Conversation

## Overview
**NEW**: Continuous voice conversation mode - like making a phone call to the AI agent!

### How It Works
```
1. User clicks green phone button 📞
2. Full-screen call UI appears
3. Agent says: "مرحباً! كيف يمكنني مساعدتك؟"
4. User starts speaking automatically
5. Agent listens → transcribes → processes → responds with voice
6. Conversation continues automatically (loop)
7. Call ends when:
   - User says "أغلق المكالمة" / "close call"
   - User clicks red "End Call" button
```

## User Experience

### Starting a Call
1. Open chat page
2. Click **green phone button** (📞) in input bar
3. Full-screen call UI appears with purple gradient background
4. Agent greets you and starts listening

### During the Call
- **NO text chat visible** - pure voice conversation
- Agent's responses shown in a floating bubble (optional visual)
- Animated avatar shows:
  - 🎤 **Pulsing microphone**: You're speaking
  - 🔊 **Pulsing speaker**: Agent is speaking
  - ⏳ **Yellow**: Processing your speech
- Background actions happen automatically (e.g., editing resume while you talk)

### Ending the Call
**Option 1**: Say these phrases:
- "أغلق المكالمة"
- "انهي المكالمة"
- "شكرا وداعا"
- "مع السلامة"
- "close call"
- "end call"
- "goodbye"

**Option 2**: Click the **red phone button** (☎️) at the bottom

---

## Technical Details

### Conversation Loop
```
┌─────────────────────────────────────┐
│  1. User Speaks                     │
│     ↓                                │
│  2. VAD detects silence → auto-stop │
│     ↓                                │
│  3. Whisper transcribes speech      │
│     ↓                                │
│  4. Check for "end call" command    │
│     ↓ (if not end)                   │
│  5. Send to agent via WebSocket     │
│     ↓                                │
│  6. Agent processes (+ actions)     │
│     ↓                                │
│  7. Agent responds (text + TTS)     │
│     ↓                                │
│  8. Auto-play audio response        │
│     ↓                                │
│  9. Wait 500ms                       │
│     ↓                                │
│ 10. START LISTENING AGAIN (loop)    │
└─────────────────────────────────────┘
```

### Key Features
✅ **Continuous listening**: Auto-restarts after agent finishes speaking  
✅ **Auto-play responses**: No clicking required  
✅ **Background actions**: Agent can edit resume, create tickets while talking  
✅ **Voice Activity Detection**: Automatically detects when you stop speaking  
✅ **Natural flow**: Like talking on the phone - no buttons needed  
✅ **Arabic optimized**: Fully supports Arabic speech and responses  

---

## Code Architecture

### New Files

#### 1. `CallMode.jsx` - Full-Screen Call UI
**Location**: `front-end/src/components/voice/CallMode.jsx`

**Features**:
- Full-screen overlay (hides chat interface)
- Animated avatar with pulsing rings
- Real-time status indicators
- Live transcript display
- End call button

**States Displayed**:
- `isListening`: User is speaking
- `isSpeaking`: Agent is speaking
- `isProcessing`: Transcribing or thinking
- `currentMessage`: What agent just said

#### 2. `useVoiceCall.js` - Call Management Hook
**Location**: `front-end/src/hooks/useVoiceCall.js`

**Functions**:
- `startCall()`: Initiates voice call session
- `endCall()`: Terminates call and cleans up
- `startListening()`: Begin recording user speech
- `stopListening()`: Stop recording and transcribe
- `sendToAgent(text)`: Send transcribed text via WebSocket
- `playAudioResponse(url)`: Auto-play agent's TTS response

**Automatic Loop Logic**:
```javascript
// After agent response audio finishes playing:
if (shouldContinueRef.current && isInCall) {
  setTimeout(() => startListening(), 500);
}
```

### Modified Files

#### `ChatPage.jsx`
- Integrated `CallMode` component
- Added `useVoiceCall` hook
- Passes `onStartCall` to `InputBar`
- CallMode overlays entire page when `isInCall === true`

#### `InputBar.jsx`
- Added **green phone button** (📞)
- Disabled text input during calls
- Disabled voice message button during calls
- Shows "المكالمة نشطة..." placeholder when in call

---

## End Call Detection

### Phrases that End the Call
The system detects these phrases (case-insensitive):

**Arabic**:
- أغلق المكالمة
- انهي المكالمة
- إنهاء المكالمة
- شكرا وداعا
- مع السلامة

**English**:
- close call
- end call
- goodbye

### Implementation
```javascript
// In useVoiceCall.js, after transcription:
const endCallPhrases = [
  'أغلق المكالمة', 'انهي المكالمة', 'إنهاء المكالمة',
  'شكرا وداعا', 'مع السلامة',
  'close call', 'end call', 'goodbye'
];

const shouldEndCall = endCallPhrases.some(phrase => 
  transcript.toLowerCase().includes(phrase.toLowerCase())
);

if (shouldEndCall) {
  endCall();
  return; // Stop the loop
}
```

---

## Example Conversations

### Example 1: Resume Update
```
👤 User: [Clicks phone button]
🤖 Agent: "مرحباً! كيف يمكنني مساعدتك؟"

👤 User: "أريد تعديل سيرتي الذاتية"
🤖 Agent: "بالتأكيد، ماذا تريد أن تعدل؟"

👤 User: "أضف مهارة البايثون"
🤖 Agent: "تم إضافة Python إلى مهاراتك. هل تريد إضافة شيء آخر؟"

👤 User: "لا، شكراً. أغلق المكالمة"
🤖 Agent: [Call ends automatically]
```

### Example 2: Q&A Session
```
👤 User: [Starts call]
🤖 Agent: "مرحباً! كيف يمكنني مساعدتك؟"

👤 User: "ما هي خدمات قوى؟"
🤖 Agent: "منصة قوى توفر خدمات توظيف وإدارة عقود العمل..." [speaks full response]

👤 User: "كيف أسجل في المنصة؟"
🤖 Agent: "لتسجيل حساب جديد..." [speaks full response]

👤 User: "شكراً، مع السلامة"
🤖 Agent: [Call ends]
```

### Example 3: Complex Task
```
👤 User: [Starts call]
🤖 Agent: "مرحباً! كيف يمكنني مساعدتك؟"

👤 User: "أريد إنشاء سيرة ذاتية جديدة"
🤖 Agent: "رائع! ما هو اسمك الكامل؟"

👤 User: "أحمد محمد العتيبي"
🤖 Agent: "شكراً أحمد. ما هو مسماك الوظيفي؟"

👤 User: "مهندس برمجيات"
🤖 Agent: "ممتاز. ما هي مهاراتك الأساسية؟"

👤 User: "بايثون وجافا سكريبت وريآكت"
🤖 Agent: "رائع. أضيف الآن... [performs action] تم إضافة المهارات. هل تريد إضافة خبراتك؟"

👤 User: "نعم، عملت في شركة تك لمدة ثلاث سنوات"
🤖 Agent: "تمام، أضيف ذلك... [performs action] تم! سيرتك الذاتية جاهزة. هل تريد شيئاً آخر؟"

👤 User: "لا، شكراً. أغلق المكالمة"
🤖 Agent: [Call ends, resume is saved]
```

---

## Comparison: Call Mode vs Text Chat

| Feature | Call Mode 📞 | Text Chat 💬 |
|---------|-------------|--------------|
| **Input** | Continuous voice | Type or single voice message |
| **Output** | Auto-play audio | Text bubbles + optional audio |
| **Flow** | Automatic loop | Manual send each message |
| **UI** | Full-screen overlay | Chat bubbles |
| **Actions** | Background (invisible) | Visible in checklist |
| **End** | Voice command or button | Always active |
| **Use Case** | Hands-free, natural conversation | Detailed review, multitasking |

---

## Testing Guide

### Test 1: Basic Call Flow
1. Click green phone button
2. Wait for "مرحباً! كيف يمكنني مساعدتك؟"
3. Say: "مرحباً"
4. Verify agent responds with audio
5. Say: "أغلق المكالمة"
6. Verify call ends, returns to chat UI

### Test 2: Resume Update via Call
1. Start call
2. Say: "أريد تعديل سيرتي الذاتية"
3. Agent asks for details
4. Provide information verbally
5. After completion, end call
6. Go to Dashboard page
7. Verify resume was updated correctly

### Test 3: Q&A via Call
1. Start call
2. Ask: "ما هي خدمات قوى؟"
3. Agent responds with audio
4. Ask follow-up question
5. Verify continuous conversation works
6. End call with button (not voice)

### Test 4: Interruption Handling
1. Start call
2. While agent is speaking, check if you can interrupt
3. Wait for agent to finish
4. System should automatically start listening
5. Speak immediately after agent finishes

### Test 5: End Call Phrases
Test each phrase:
- "أغلق المكالمة" ✓
- "انهي المكالمة" ✓
- "مع السلامة" ✓
- "close call" ✓
- "goodbye" ✓

---

## Troubleshooting

### Issue 1: Call doesn't start
**Symptom**: Click phone button, nothing happens  
**Cause**: WebSocket not connected  
**Solution**:
1. Check backend is running
2. Refresh page
3. Wait for "Connected" status in console

### Issue 2: Agent doesn't respond
**Symptom**: You speak, but no response  
**Cause**: WebSocket disconnected mid-call  
**Solution**:
1. End call
2. Check backend logs
3. Restart call

### Issue 3: Audio doesn't auto-play
**Symptom**: Call continues but no audio  
**Cause**: Browser blocked autoplay  
**Solution**:
1. Chrome: Settings → Privacy → Site Settings → Sound → Allow
2. Or interact with page first (click anywhere)

### Issue 4: Call doesn't end with voice command
**Symptom**: Say "أغلق المكالمة" but call continues  
**Cause**: Transcription error or phrase not detected  
**Solution**:
1. Speak clearly: "أغلق المكالمة"
2. Or use red end call button

### Issue 5: Loop doesn't restart
**Symptom**: Agent speaks, then silence  
**Cause**: `shouldContinueRef` was set to false  
**Solution**:
1. Check console for errors
2. End and restart call

---

## Configuration

### Adjust Auto-Listen Delay
**File**: `useVoiceCall.js`

```javascript
// After audio finishes:
setTimeout(() => startListening(), 500); // Change 500ms to your preference
```

**Recommendations**:
- **Fast pace**: 300ms
- **Normal**: 500ms (current)
- **Relaxed**: 1000ms

### Customize End Call Phrases
**File**: `useVoiceCall.js`

```javascript
const endCallPhrases = [
  'أغلق المكالمة',
  'bye bye', // Add your own
  // ... more phrases
];
```

### Change Call UI Colors
**File**: `CallMode.jsx`

```javascript
className="fixed inset-0 bg-gradient-to-br from-qiwa-primary via-purple-600 to-qiwa-secondary"
```

Change gradient colors to match your brand.

---

## Performance

### Latency per Turn
| Stage | Duration |
|-------|----------|
| User speaks | 2-5 seconds |
| VAD detects end | ~1 second |
| Transcription (Whisper) | 2-4 seconds |
| Agent processing | 2-5 seconds |
| TTS generation | 1-2 seconds |
| Audio playback | 3-10 seconds (depends on response length) |
| **Total per turn** | **11-27 seconds** |

### Optimizations
1. **Use `tts-1` model** (faster than `tts-1-hd`)
2. **Keep responses concise** (shorter audio = faster)
3. **Parallel processing**: TTS generates while agent is still thinking

---

## Cost per Call

**5-minute conversation** (~10 turns):

| Item | Cost |
|------|------|
| 10× Whisper transcriptions (~30s each) | $0.03 |
| 10× GPT-4o-mini calls | $0.001 |
| 10× TTS responses (~100 chars each) | $0.015 |
| **Total** | **~$0.05 per 5-min call** |

**100 calls/day** = $5/day = **$150/month**

---

## Summary

✅ **Implemented**:
- Full-screen call UI with animations
- Continuous voice loop (automatic)
- Auto-play agent responses
- End call detection (voice + button)
- Background action execution
- WebSocket integration
- Arabic-optimized

✅ **User Experience**:
- Like making a phone call
- No text chat visible during call
- Hands-free conversation
- Natural flow with automatic turns

✅ **Technical**:
- 3 new files created
- 2 files modified
- Fully integrated with existing backend
- No backend changes needed (uses existing WebSocket/TTS/STT)

🎉 **Ready to use!** Click the green phone button and start talking! 📞


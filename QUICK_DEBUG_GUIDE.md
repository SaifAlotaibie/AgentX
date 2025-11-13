# 🔧 Quick Debug Guide - Voice Call Not Working

## Step 1: Check Browser Console

1. Open your browser (Chrome/Firefox)
2. Press **F12** or **Cmd+Option+I** (Mac)
3. Click the **Console** tab
4. Click the green phone button (📞)
5. **Look for errors in red**

### What to look for:

#### ✅ **Good Signs** (means it's working):
```
[Call] Starting call...
[Call] WebSocket connected
[Call] Starting to listen...
```

#### ❌ **Bad Signs** (errors):

**Error 1**: `Cannot find module '@ricky0123/vad-react'`
```
Solution: Run this in front-end folder:
npm install
```

**Error 2**: `WebSocket connection failed`
```
Solution: Backend not running! Start it:
cd backend/Agents
python3 -m uvicorn app:app --reload --port 8000
```

**Error 3**: `Microphone permission denied`
```
Solution: 
1. Click the lock icon in browser address bar
2. Allow microphone access
3. Refresh page
```

**Error 4**: `useMicVAD is not a function`
```
Solution: VAD library issue (I've disabled it now - should work)
```

---

## Step 2: Test Simplified Version

I've disabled the VAD (Voice Activity Detection) for now to make it simpler:

### How it works now:
1. Click green phone button 📞
2. Full-screen appears
3. You speak for **5 seconds** (auto-stops)
4. Agent processes and responds
5. Repeat

**Note**: Instead of auto-detecting when you stop speaking, it now records for 5 seconds then stops automatically.

---

## Step 3: Restart Everything

```bash
# 1. Stop frontend (Ctrl+C in terminal)
# 2. Restart it:
cd /Users/ziyadalharbi/AgentX_hackathon/AgentX/front-end
npm run dev

# 3. Make sure backend is running:
cd /Users/ziyadalharbi/AgentX_hackathon/AgentX/backend/Agents
python3 -m uvicorn app:app --reload --port 8000
```

---

## Step 4: Test Again

1. Open chat page
2. Open console (F12)
3. Click green phone button
4. Watch console for messages
5. **Tell me what you see!**

---

## Common Issues & Solutions

### Issue: Button doesn't do anything
**Check**: Console errors?
**Fix**: Tell me what the error says

### Issue: Full-screen appears but no greeting
**Check**: Is backend running?
**Fix**: Start backend

### Issue: "Permission denied"
**Check**: Microphone access blocked?
**Fix**: Allow in browser settings

### Issue: Call starts but no response
**Check**: Backend logs for errors
**Fix**: Check `/backend/Agents` terminal

---

## What Changed

**Before** (what I tried first):
- VAD auto-detects silence
- Complex voice activity detection

**Now** (simpler):
- 5-second auto-stop
- No VAD library needed
- Easier to debug

---

## Next Steps

After you click the button and check the console, tell me:

1. ✅ **If it works**: Great! We can re-enable VAD later
2. ❌ **If it doesn't work**: Copy/paste the error message from console

I'm here to help debug! 🔧


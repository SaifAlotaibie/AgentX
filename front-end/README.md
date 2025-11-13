# Qiwa Assistant - Frontend

Beautiful, modern React frontend for the Qiwa AI Customer Service Agent.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 🎮 Mock Mode vs Real Backend

The frontend has two modes:

### Mock Mode (Default - for testing)
- Simulates backend responses locally
- No need for Python backend to be running
- Perfect for UI development and demo
- Edit `.env` and set: `VITE_MOCK_MODE=true`

### Real Backend Mode
- Connects to actual Python WebSocket backend
- Make sure backend is running on `localhost:8000`
- Edit `.env` and set: `VITE_MOCK_MODE=false`

## 📂 Project Structure

```
src/
├── components/
│   ├── chat/              # Chat interface components
│   │   ├── ChatArea.jsx
│   │   ├── MessageBubble.jsx
│   │   ├── InputBar.jsx
│   │   ├── Checklist.jsx
│   │   └── TypingIndicator.jsx
│   ├── sidebar/           # Sidebar components
│   │   ├── TicketsTab.jsx
│   │   ├── DashboardTab.jsx
│   │   └── TicketCard.jsx
│   └── layout/            # Layout components
│       ├── Header.jsx
│       ├── Sidebar.jsx
│       └── MainLayout.jsx
├── hooks/
│   ├── useWebSocket.js    # WebSocket connection hook
│   └── useVoiceInput.js   # Voice input hook
├── store/
│   └── chatStore.js       # Zustand state management
├── lib/
│   └── utils.js           # Utility functions
├── App.jsx
└── main.jsx
```

## ✨ Features

### ✅ Implemented
- 💬 Real-time chat interface with beautiful animations
- 📋 Live process checklist that updates as agent works
- 🎤 Voice input support (both Arabic & English)
- 🎫 Ticket management sidebar
- 📊 Dashboard with statistics
- 🌐 Bilingual support (auto-detects Arabic/English)
- 🔄 WebSocket connection with auto-reconnect
- 🎨 Modern UI with Tailwind CSS
- ⚡ Smooth animations with Framer Motion
- 📱 Responsive design

### 🎨 UI Components
- Message bubbles (user & assistant)
- Typing indicator (3 dots animation)
- Process checklist with status icons
- Quick action buttons
- Connection status indicator
- Ticket cards with type-based colors
- Dashboard stats cards

## 🎯 How to Use

### Testing in Mock Mode

1. **Start the frontend** (backend not needed):
   ```bash
   npm run dev
   ```

2. **Open in browser**: `http://localhost:5173`

3. **Try these messages**:
   - "I want to add my resume"
   - "أريد إضافة سيرتي الذاتية"
   - "What is Qiwa?"

4. **Watch the magic**:
   - See real-time checklist updates
   - Tickets appear in sidebar
   - Dashboard stats update

### Testing with Real Backend

1. **Start Python backend**:
   ```bash
   cd backend/Agents
   uvicorn app:app --reload
   ```

2. **Update `.env`**:
   ```
   VITE_MOCK_MODE=false
   ```

3. **Start frontend**:
   ```bash
   npm run dev
   ```

4. **Test the full flow**!

## 🎤 Voice Input

The app supports voice input in both Arabic and English:

1. Click the microphone button 🎤
2. Grant microphone permission (first time)
3. Speak your message
4. Click again to stop
5. Edit if needed, then send

## 🎫 Sidebar Features

### Tickets Tab
- Shows all created tickets
- Color-coded by type (Add/Edit/Delete)
- Real-time status updates
- Open/Closed count

### Dashboard Tab
- Total messages count
- Active tickets
- Session information
- Quick stats

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change the theme:
```javascript
colors: {
  qiwa: {
    primary: '#667eea',    // Purple
    secondary: '#764ba2',  // Dark purple
    accent: '#f093fb',     // Pink
  }
}
```

### WebSocket URL
Edit `.env`:
```
VITE_WS_URL=ws://your-backend-url:8000
```

## 🐛 Troubleshooting

### "Connection failed"
- Make sure backend is running if mock mode is off
- Check `.env` VITE_MOCK_MODE setting
- Verify WebSocket URL is correct

### Voice input not working
- Check browser permissions
- Chrome/Edge work best
- Safari may have limited support

### Styles not loading
- Run `npm install` again
- Clear browser cache
- Check console for errors

## 📦 Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## 🛠️ Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Zustand** - State management
- **Lucide React** - Icons
- **Web Speech API** - Voice input

## 🚀 Next Steps

1. Connect to real backend (set VITE_MOCK_MODE=false)
2. Test end-to-end flows
3. Customize colors/branding
4. Add more quick action buttons
5. Deploy to production

## 📝 Notes

- The UI auto-detects Arabic text and applies RTL layout
- All timestamps are in local time
- Session ID is generated on page load
- WebSocket auto-reconnects if connection drops

---

Built with ❤️ for Qiwa Platform

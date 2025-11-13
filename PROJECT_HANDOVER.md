# 🚀 **PROJECT HANDOVER DOCUMENT**
## **Qiwa AI Customer Service Agent - Complete Guide**

---

## 📌 **PROJECT OVERVIEW**

### **What is this project?**
An **AI-powered customer service agent** for the **Qiwa platform** (Saudi Arabia's employment platform). The system serves three user types:
1. **Employees** - Resume management, contract viewing, certificate requests
2. **Business Owners** - Work permit management, employee oversight
3. **Service Providers** - End-of-service reward calculations

### **Main Capabilities:**
- **Natural Language Interface** (Arabic primary, English support)
- **Voice Interaction** (Speech-to-Text + Text-to-Speech)
- **Real-time Updates** (WebSocket-based communication)
- **Multi-feature Agent** (9 major features implemented)
- **Persistent Storage** (Dual: JSON files + Supabase database)

### **Current Status:**
✅ **MVP Complete** - Core features fully functional  
✅ **Voice Mode** - Continuous phone-call-like experience  
✅ **Dashboard** - 5 tabs with real-time data  
✅ **Database Integration** - Supabase connected  
🔧 **Development Mode** - All features accessible for testing

---

## 🛠️ **TECH STACK**

### **Backend:**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.x | Core language |
| **FastAPI** | ≥0.104.0 | Web server + WebSocket |
| **Uvicorn** | ≥0.24.0 | ASGI server |
| **LangChain** | ≥0.1.0 | LLM orchestration |
| **LangGraph** | ≥0.0.20 | Agent workflow |
| **OpenAI** | ≥1.3.0 | GPT-4o-mini + Whisper + TTS |
| **Supabase** | ≥2.0.0 | Database (PostgreSQL) |
| **Pydantic** | ≥2.0.0 | Data validation |

### **Frontend:**
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.0 | UI framework |
| **Vite** | 7.2.2 | Build tool |
| **TailwindCSS** | 3.4.0 | Styling |
| **Framer Motion** | 12.23.24 | Animations |
| **React Router** | 7.9.5 | Navigation |
| **Zustand** | 5.0.8 | State management |
| **@ricky0123/vad-react** | 0.0.35 | Voice Activity Detection |
| **Lucide React** | 0.553.0 | Icons |

### **Database:**
- **Supabase (PostgreSQL)** - Production database
- **JSON Files** - Development/backup storage

### **APIs:**
- **OpenAI API** - GPT-4o-mini (chat), Whisper (STT), TTS (voice)
- **Supabase API** - Database operations

---

## ✅ **CURRENT FEATURES IMPLEMENTED**

### **Core Features (MVP):**
1. ✅ **Resume Management** - Add, edit, delete resumes (with education/experience validation)
2. ✅ **Ticket System** - Open, track, close support tickets
3. ✅ **Knowledge Q&A** - Answer questions about Qiwa services

### **New Features (Scaling Phase):**
4. ✅ **Contract Management** - View employment contracts
5. ✅ **Certificate Requests** - Request salary/experience certificates
6. ✅ **Work Permit Management** - View, check expiry, renew permits (business owners)
7. ✅ **End-of-Service Calculator** - Calculate rewards per Saudi labor law
8. ✅ **Proactive Reminders** - System-generated notifications for important events

### **UI Features:**
9. ✅ **Voice Call Mode** - Continuous phone-call experience with VAD
10. ✅ **Real-time Checklist** - Process step tracking during agent operations
11. ✅ **Dashboard** - 5 tabs (Resumes, Contracts, Certificates, Work Permits, Reminders)
12. ✅ **Multi-page Navigation** - HRSD Home → Qiwa Main → Chat

### **Agent Intelligence:**
- ✅ **LLM Function Calling** - Real AI decision-making (not rule-based)
- ✅ **Context Memory** - Remembers last accessed resume across sessions
- ✅ **Bilingual** - Arabic primary (forced), English fallback

---

## 📁 **FOLDER STRUCTURE & KEY FILES**

```
AgentX/
├── backend/Agents/          # Backend agent system
│   ├── agents/              # Agent implementations
│   │   ├── real_agent.py    # ⭐ MAIN: LLM-based agent with function calling
│   │   ├── employee_agent.py # (OLD: Rule-based, not used)
│   │   └── base_agent.py    # Base agent class
│   │
│   ├── routers/             # FastAPI route handlers
│   │   ├── real_employee_router.py  # ⭐ MAIN: Handles chat sessions & routing
│   │   └── employee_router.py       # (OLD: Not used)
│   │
│   ├── tools/               # Agent tools (actions the AI can take)
│   │   ├── employee/        # Employee-specific tools
│   │   │   ├── resume_tool.py       # Resume CRUD operations
│   │   │   ├── contract_tool.py     # View contracts
│   │   │   └── certificate_tool.py  # Request certificates
│   │   ├── business/        # Business owner tools
│   │   │   └── work_permit_tool.py  # Manage work permits
│   │   ├── provider/        # Service provider tools
│   │   │   └── reward_calculator_tool.py  # Calculate rewards
│   │   └── shared/          # Tools for all user types
│   │       ├── ticket_tool.py       # Ticket management
│   │       ├── knowledge_tool.py    # Q&A
│   │       └── reminder_tool.py     # Reminders
│   │
│   ├── storage/             # JSON file storage (primary for dev)
│   │   ├── resume_storage.py
│   │   ├── contract_storage.py
│   │   ├── certificate_storage.py
│   │   ├── work_permit_storage.py
│   │   ├── ticket_storage.py
│   │   └── reminder_storage.py
│   │
│   ├── database/            # Supabase integration (secondary)
│   │   ├── supabase_client.py       # ⭐ Supabase initialization
│   │   ├── supabase_storage.py      # ⭐ 11+ storage classes for DB
│   │   └── schema.sql               # ⭐ Database schema (11 tables)
│   │
│   ├── config/
│   │   └── settings.py      # ⭐ CONFIGURATION: API keys, flags, paths
│   │
│   ├── utils/
│   │   ├── logger.py        # JSONL logging
│   │   └── llm_wrapper.py   # LLM call wrapper
│   │
│   ├── app.py               # ⭐ MAIN SERVER: FastAPI + WebSocket
│   ├── requirements.txt     # Python dependencies
│   └── seed_demo_data.py    # ⭐ Populates demo data
│
├── front-end/               # React frontend
│   ├── src/
│   │   ├── pages/           # Main pages
│   │   │   ├── ChatPage.jsx         # ⭐ Main chat interface
│   │   │   ├── DashboardPage.jsx    # ⭐ Multi-tab dashboard
│   │   │   ├── TicketsPage.jsx
│   │   │   ├── HRSDHomePage.jsx     # Landing page
│   │   │   └── QiwaMainPage.jsx     # Qiwa services page
│   │   │
│   │   ├── components/
│   │   │   ├── chat/        # Chat UI components
│   │   │   │   ├── ChatArea.jsx
│   │   │   │   ├── InputBar.jsx
│   │   │   │   ├── MessageBubble.jsx
│   │   │   │   ├── Checklist.jsx
│   │   │   │   └── TypingIndicator.jsx
│   │   │   ├── dashboard/   # Dashboard tab components
│   │   │   │   ├── ResumesTab.jsx
│   │   │   │   ├── ContractsTab.jsx
│   │   │   │   ├── CertificatesTab.jsx
│   │   │   │   ├── WorkPermitsTab.jsx
│   │   │   │   └── RemindersTab.jsx
│   │   │   ├── voice/
│   │   │   │   └── CallMode.jsx     # ⭐ Voice call UI overlay
│   │   │   └── layout/      # Navigation, Header, Sidebar
│   │   │
│   │   ├── hooks/           # Custom React hooks
│   │   │   ├── useWebSocket.js      # ⭐ WebSocket connection
│   │   │   ├── useVoiceCall.js      # ⭐ Voice call logic
│   │   │   ├── useVoiceInput.js     # Speech-to-Text
│   │   │   └── useAudioPlayer.js    # Text-to-Speech playback
│   │   │
│   │   ├── store/
│   │   │   └── chatStore.js         # ⭐ Zustand state management
│   │   │
│   │   ├── config/
│   │   │   └── mockUser.js          # ⭐ Mock user for testing
│   │   │
│   │   ├── lib/
│   │   │   └── supabase.js          # Supabase client init
│   │   │
│   │   ├── App.jsx          # ⭐ Main app component + routing
│   │   └── main.jsx         # Entry point
│   │
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
│
├── data/                    # Static data files
│   ├── hrsd_faqs_rag.json   # FAQ data for RAG (future)
│   └── services_converted.json  # Qiwa services list
│
└── *.md                     # Documentation files
    ├── FEATURES_SUMMARY.md
    ├── TESTING_GUIDE.md
    ├── DATABASE_INTEGRATION.md
    ├── VOICE_CALL_MODE.md
    └── README.md
```

---

## 🚀 **HOW TO RUN THE PROJECT**

### **Prerequisites:**
- Python 3.x
- Node.js & npm
- OpenAI API key
- Supabase account (optional for dev)

### **1. Backend Setup:**

```bash
cd backend/Agents

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env
```

**`.env` file contents:**
```env
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=sk-...your-key-here...

# Supabase (Already configured with defaults, but can override)
SUPABASE_URL=https://womyztswwrnyazqglryg.supabase.co
SUPABASE_KEY=eyJhbGci...your-key...

# Model Configuration (Optional)
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

**Seed demo data:**
```bash
python3 seed_demo_data.py
```

**Start the backend:**
```bash
python3 app.py
```

✅ Backend runs on `http://localhost:8000`

### **2. Frontend Setup:**

```bash
cd front-end

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend runs on `http://localhost:5173`

### **3. Verify Setup:**

1. **Backend Health Check:** `http://localhost:8000/health`
2. **Frontend:** `http://localhost:5173`
3. **WebSocket Test:** Open browser console, should see "WebSocket connected"

---

## 💾 **DATA USED / NEEDED**

### **Current Demo Data (Seeded):**

| Data Type | Count | Location |
|-----------|-------|----------|
| **Resumes** | 6 | `logs/resumes/demo_user_resumes.json` |
| **Contracts** | 2 | `logs/contracts/demo_user_contracts.json` |
| **Certificates** | 3 | `logs/certificates/demo_user_certificates.json` |
| **Work Permits** | 5 | `logs/work_permits/EST12345_permits.json` |
| **Reminders** | 4 | `logs/reminders/demo_user_reminders.json` |

### **Data Structure Examples:**

**Resume:**
```json
{
  "resumeId": "RE8AE450D",
  "data": {
    "full_name": "زياد الحربي",
    "job_title": "مهندس ذكاء اصطناعي",
    "contact": {
      "email": "ziyad@test.com",
      "phone": "0544123456"
    },
    "education": [
      {
        "school": "جامعة ستانفورد",
        "degree": "ماجستير ذكاء اصطناعي",
        "year": "2022"
      }
    ],
    "experience": [
      {
        "company": "شركة علي بابا",
        "role": "مهندس ذكاء اصطناعي",
        "start_date": "2022",
        "end_date": "الآن"
      }
    ]
  }
}
```

**Contract:**
```json
{
  "contractId": "CONBC02ABEF",
  "data": {
    "employer_name": "شركة أرامكو السعودية",
    "job_title": "مهندس برمجيات أول",
    "salary": 15000.00,
    "start_date": "2022-01-01",
    "end_date": "2025-01-01",
    "status": "active"
  }
}
```

### **Future Data Needs:**
- Real user authentication system
- Connection to actual Qiwa API (not available yet)
- RAG system for knowledge base (FAQ data exists in `/data/`)
- User profile management (partially implemented)

---

## 🔌 **INTEGRATION NOTES**

### **Backend ↔ Frontend Communication:**

**Protocol:** WebSockets  
**Endpoint:** `ws://localhost:8000/ws/{sessionId}/{userId}/{userRole}`

**Message Types:**
1. **`user_message`** - User sends text/voice to agent
   ```json
   {
     "type": "user_message",
     "message": "أريد رؤية عقدي",
     "sessionId": "S123",
     "userId": "demo_user",
     "userRole": "employee"
   }
   ```

2. **`chat_message`** - Agent responds to user
   ```json
   {
     "type": "chat_message",
     "role": "assistant",
     "message": "عقدك مع شركة أرامكو...",
     "timestamp": "2025-11-13T..."
   }
   ```

3. **`process_update`** - Real-time checklist updates
   ```json
   {
     "type": "process_update",
     "steps": [
       {"id": "open_ticket", "status": "done"},
       {"id": "gather_info", "status": "in_progress"}
     ]
   }
   ```

4. **`audio_response`** - TTS audio file URL
   ```json
   {
     "type": "audio_response",
     "audioUrl": "http://localhost:8000/api/audio/response_123.mp3"
   }
   ```

### **Agent → Supabase:**
- **Dual Storage:** All data writes go to BOTH JSON files and Supabase
- **Non-blocking:** Supabase writes don't fail the operation if DB is down
- **Logging:** Tool calls, process steps, conversations stored in DB

### **Frontend → Backend REST APIs:**
```
GET  /resumes/{userId}           # Fetch all resumes
GET  /contracts/{userId}         # Fetch all contracts
GET  /certificates/{userId}      # Fetch all certificates
GET  /permits/{establishmentId}  # Fetch work permits
GET  /reminders/{userId}         # Fetch reminders
GET  /tickets/{userId}           # Fetch support tickets
POST /api/transcribe             # Whisper STT endpoint
GET  /api/audio/{filename}       # Serve TTS audio files
```

---

## ⚠️ **KNOWN ISSUES / TODOS**

### **Current Issues:**
1. ⚠️ **Work Permits Dashboard Tab** - Not visible for non-business-owners in UI (intended behavior, but should be accessible in dev mode via dashboard)
2. ⚠️ **Voice Call Latency** - ~2-3 second delay in agent response (OpenAI API limitation)
3. ⚠️ **Resume Context** - Sometimes agent still asks for resume ID even with persistent context (rare)
4. ⚠️ **Supabase Schema** - Some old data may not migrate cleanly (run `SUPABASE_MIGRATION_V2.sql` fresh)

### **TODOs (Backlog):**

#### **High Priority:**
- [ ] **Real Authentication** - Replace mock user with actual login system
- [ ] **Production Mode** - Set `DEV_MODE_ALL_FEATURES = False` and test user-type restrictions
- [ ] **Error Handling** - Better user-facing error messages (currently shows technical errors)
- [ ] **Voice Optimization** - Reduce latency (consider local TTS like ElevenLabs)

#### **Medium Priority:**
- [ ] **RAG Implementation** - Use `data/hrsd_faqs_rag.json` for knowledge base
- [ ] **Multi-language** - Proper English support (currently Arabic-only)
- [ ] **Dashboard Interactivity** - Make dashboard cards clickable/editable
- [ ] **Ticket Actions** - Allow re-opening closed tickets
- [ ] **File Upload** - Upload resume PDFs, contract documents

#### **Low Priority:**
- [ ] **Agent Personalization** - Learn user preferences over time
- [ ] **Analytics Dashboard** - Track usage, popular features, success rates
- [ ] **Dark Mode** - UI theme switcher

### **Testing Gaps:**
- ⚠️ No automated tests (all manual testing so far)
- ⚠️ Edge cases not fully tested (e.g., very long conversations, network interruptions)
- ⚠️ Load testing not performed (1 user works, 100 users untested)

---

## 🎯 **NEXT STEP SUGGESTIONS**

### **For Immediate Continuation:**

1. **Improve Voice Experience (High Impact)**
   - Implement streaming TTS for faster responses
   - Add background noise cancellation
   - Better VAD tuning for Arabic speech

2. **Complete Dashboard Interactivity**
   - Make contract cards expandable
   - Add "Download PDF" functionality for certificates
   - Implement reminder dismissal/snooze

3. **Production Readiness**
   - Set up proper authentication (OAuth2, Supabase Auth)
   - Configure production environment variables
   - Set `DEV_MODE_ALL_FEATURES = False`
   - Add rate limiting

4. **RAG System**
   - Integrate `data/hrsd_faqs_rag.json` into `knowledge_tool.py`
   - Use vector database (Pinecone/Chroma/Supabase Vector)
   - Implement semantic search for Q&A

5. **Testing & Quality**
   - Write unit tests for tools (pytest)
   - Add integration tests for agent workflows
   - Set up CI/CD (GitHub Actions)

### **For Long-term Scaling:**

6. **Multi-tenancy**
   - Separate data per organization
   - Admin dashboard for managing users

7. **Real Qiwa API Integration**
   - Replace mock data with real API calls
   - Handle API authentication/rate limits

8. **Advanced Features**
   - Document parsing (extract resume data from PDFs)
   - Email notifications for certificate readiness
   - Scheduled reminders (cron jobs)

9. **Performance Optimization**
   - Cache frequently accessed data (Redis)
   - Optimize database queries
   - Implement WebSocket connection pooling

10. **Monitoring & Observability**
    - Set up logging infrastructure (ELK stack)
    - Error tracking (Sentry)
    - Performance monitoring (New Relic/DataDog)

---

## 📚 **HELPFUL DOCUMENTATION FILES**

| File | Description |
|------|-------------|
| `FEATURES_SUMMARY.md` | Quick overview of all features |
| `TESTING_GUIDE.md` | ⭐ Step-by-step testing instructions |
| `DATABASE_INTEGRATION.md` | Supabase schema and integration details |
| `VOICE_CALL_MODE.md` | Voice feature architecture |
| `COMPLETE_REBUILD_SUMMARY.md` | Technical implementation details |
| `QUICK_DEBUG_GUIDE.md` | Common issues and fixes |

---

## 🤝 **DEVELOPMENT TIPS**

### **Using Cursor AI:**
- The project has extensive inline comments
- Each tool has clear docstrings
- Use `@workspace` to reference project structure
- Most complex logic is in:
  - `backend/Agents/agents/real_agent.py`
  - `backend/Agents/routers/real_employee_router.py`
  - `front-end/src/hooks/useVoiceCall.js`

### **Debugging:**
- **Backend logs:** Check `backend/Agents/logs/` folder
- **Frontend logs:** Browser console (F12)
- **WebSocket traffic:** Browser Network tab → WS
- **Database:** Supabase dashboard → Table Editor

### **Making Changes:**
- **Add new tool:** Create in `backend/Agents/tools/`, import in `real_agent.py`
- **Add new feature:** Update both storage (JSON + Supabase) and frontend tab
- **Change agent behavior:** Modify system prompt in `real_agent.py`

---

## 📞 **CONTACT & HANDOVER NOTES**

### **From Ziyad:**
- This project took ~2 weeks of intensive development
- Most decisions were made iteratively based on testing
- The current architecture is solid but can be improved
- **Development mode** is enabled for easy testing - remember to disable in production!
- All Supabase credentials are already configured (your friend's account)
- Mock user is set up for quick testing without auth

### **Key Design Decisions:**
1. **Dual Storage** - JSON for development speed, Supabase for production analytics
2. **LLM Function Calling** - Real AI agent, not rule-based (more flexible but less predictable)
3. **WebSocket** - Real-time communication is core to UX
4. **Arabic-First** - All responses forced to Arabic (can be toggled in settings)
5. **Development Mode** - Allows testing all features without user type restrictions

### **What Works Well:**
- ✅ Voice call experience is smooth
- ✅ Real-time updates feel instant
- ✅ Agent is quite intelligent with function calling
- ✅ Dashboard UI is clean and functional

### **What Needs Work:**
- ⚠️ Voice latency (2-3 seconds)
- ⚠️ No real authentication yet
- ⚠️ Edge cases in conversations

---

## 🎉 **FINAL CHECKLIST FOR YOUR FRIEND**

Before starting development, verify:
- [ ] Backend runs: `python3 app.py` in `backend/Agents/`
- [ ] Frontend runs: `npm run dev` in `front-end/`
- [ ] Demo data seeded: `python3 seed_demo_data.py`
- [ ] OpenAI API key configured in `.env`
- [ ] Can chat with agent: `http://localhost:5173/chat`
- [ ] Dashboard loads: `http://localhost:5173/dashboard`
- [ ] Voice call works (green phone button)
- [ ] Read `TESTING_GUIDE.md` for feature testing

**Good luck! The foundation is solid. Build something amazing! 🚀**

---

*This document was prepared by Ziyad for project handover. Last updated: November 13, 2025.*


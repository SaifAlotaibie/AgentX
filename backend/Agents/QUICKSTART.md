# Quick Start Guide - Qiwa Agent System

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd backend/Agents
pip install -r requirements.txt
```

### Step 2: Configure Environment (Optional for Testing)

The system works without an OpenAI API key for basic testing. To use actual LLM features:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 3: Run Tests

```bash
python3 test_agent.py
```

You should see all tests pass ✓

### Step 4: Start the Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

### Step 5: Test the Agent

#### Option A: Use the Web Client

1. Open `sample_client.html` in your browser
2. Click "Connect"
3. Try these messages:
   - "I want to add my resume"
   - "أريد إضافة سيرتي الذاتية"
   - "What is Qiwa?"
   - "ما هي منصة قوى؟"

#### Option B: Use cURL

```bash
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "S123",
    "userId": "U123",
    "userRole": "employee",
    "message": "I want to add my resume"
  }'
```

#### Option C: Use Python

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/message",
    json={
        "sessionId": "S123",
        "userId": "U123",
        "userRole": "employee",
        "message": "What is Qiwa?"
    }
)

print(response.json())
```

## 📊 Check the Logs

```bash
# View chat logs
tail -f logs/chat_logs.jsonl | jq

# View actions
tail -f logs/actions.jsonl | jq

# View LLM calls (if using OpenAI)
tail -f logs/llm.jsonl | jq
```

## 🎯 What You Can Do

### Resume Management (Arabic & English)

1. **Add Resume**: "I want to add my resume" / "أريد إضافة سيرتي الذاتية"
   - Agent will ask for: name, job title, email, phone
   - Creates ticket automatically
   - Tracks progress with real-time checklist

2. **Edit Resume**: "I want to edit my resume" / "أريد تعديل سيرتي الذاتية"
   - Agent will ask what section to edit
   - Updates the resume
   - Closes ticket on confirmation

3. **Delete Resume**: "Delete my resume" / "احذف سيرتي الذاتية"
   - Agent will ask for confirmation
   - Deletes the resume

### Q&A (Arabic & English)

Ask questions about Qiwa:
- "What is Qiwa?" / "ما هي منصة قوى؟"
- "How do I register?" / "كيف أسجل؟"
- Questions about services from the FAQ database

## 🔧 API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `WS /ws/{sessionId}/{userId}/{userRole}` - WebSocket connection
- `POST /agent/message` - HTTP message endpoint
- `GET /session/{sessionId}` - Get session state
- `DELETE /session/{sessionId}` - Clear session

## 📝 Real-Time Events

When you connect via WebSocket, you'll receive:

1. **chat_message** - Assistant responses
2. **process_update** - Checklist updates with step status
3. **ticket_update** - Ticket opened/closed
4. **final_response** - Final result of the operation

## 🌟 Features

- ✅ Bilingual (Arabic & English)
- ✅ Real-time WebSocket updates
- ✅ Automatic ticket management
- ✅ Process tracking with checklist
- ✅ Conversation memory
- ✅ Structured logging
- ✅ FAQ-based Q&A
- ✅ Resume CRUD operations

## 🔮 Next Steps

1. **Add OpenAI API Key**: For actual LLM-powered responses
2. **Connect Backend**: Replace simulated API calls in tools
3. **Integrate RAG**: Replace keyword matching with vector search
4. **Add More Roles**: Implement business_owner and service_provider routers

## 💡 Tips

- Session IDs persist conversation context
- User IDs link to backend user accounts
- All interactions are logged for analytics
- The system works offline for testing (no API key needed)

## 🐛 Troubleshooting

**ModuleNotFoundError**: Install dependencies
```bash
pip install -r requirements.txt
```

**Port already in use**: Change port in .env or use different port
```bash
uvicorn app:app --port 8001
```

**WebSocket connection fails**: Test HTTP endpoint first
```bash
curl http://localhost:8000/health
```

## 📚 Documentation

See `README.md` for complete documentation.

---

Built with ❤️ for Qiwa Platform


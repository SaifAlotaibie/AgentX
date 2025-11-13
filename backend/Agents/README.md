# Qiwa Agent System - MVP

AI-powered customer service agent for the Qiwa platform, supporting resume management and Q&A for employees.

## Features

- **Resume Management**: Add, edit, and delete employee resumes through conversational chat
- **Q&A System**: Answer questions using FAQ database with Arabic and English support
- **Bilingual Support**: Full support for both Arabic and English
- **Real-time Updates**: WebSocket-based real-time checklist updates for process tracking
- **Ticket Management**: Automatic ticket creation and management for resume operations
- **Structured Logging**: All interactions logged to JSONL files for analytics

## Architecture

- **LangChain + LangGraph**: Agent orchestration and state management
- **FastAPI + WebSocket**: Real-time communication
- **OpenAI GPT-4o-mini**: LLM for intelligent responses (with stubs for local models)
- **JSON-based FAQ**: Simple keyword matching (ready for RAG integration)

## Project Structure

```
backend/Agents/
├── app.py                      # FastAPI WebSocket server
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   └── settings.py            # Configuration management
├── routers/
│   └── employee_router.py     # Employee request handler
├── agents/
│   ├── base_agent.py          # LangGraph state definition
│   └── employee_agent.py      # Employee agent graph
├── tools/
│   ├── employee/
│   │   └── resume_tool.py     # Resume CRUD operations
│   └── shared/
│       ├── ticket_tool.py     # Ticket management
│       └── knowledge_tool.py  # Q&A with FAQ data
├── memory/
│   └── conversation_memory.py # Session persistence
├── utils/
│   ├── logger.py              # Structured JSON logging
│   ├── llm_wrapper.py         # LLM call wrapper
│   └── language_detector.py   # Language detection
└── logs/                      # Log files (auto-created)
    ├── chat_logs.jsonl
    ├── actions.jsonl
    ├── errors.jsonl
    ├── llm.jsonl
    └── sessions/              # Session memory files
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager
- OpenAI API key

### Installation

1. **Navigate to the Agents directory**:
   ```bash
   cd backend/Agents
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Verify FAQ data files exist**:
   - Ensure `/data/hrsd_faqs_rag.json` exists
   - Ensure `/data/services_converted.json` exists

## Running the Server

### Development Mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check

```bash
GET /health
```

Returns server status.

### WebSocket Connection

```
ws://localhost:8000/ws/{sessionId}/{userId}/{userRole}
```

**Parameters**:
- `sessionId`: Unique session identifier
- `userId`: User identifier
- `userRole`: User role (currently supports `employee`)

**Message Format** (Client → Server):
```json
{
  "type": "user_message",
  "message": "I want to add my resume",
  "sessionId": "S123",
  "userId": "U123",
  "userRole": "employee"
}
```

**Event Types** (Server → Client):
- `chat_message`: Assistant messages
- `process_update`: Checklist updates
- `ticket_update`: Ticket status changes
- `final_response`: Final result

### HTTP Fallback

```bash
POST /agent/message
```

**Request Body**:
```json
{
  "sessionId": "S123",
  "userId": "U123",
  "userRole": "employee",
  "message": "I want to add my resume"
}
```

**Response**:
```json
{
  "status": "success",
  "sessionId": "S123",
  "messages": [...],
  "finalResponse": {...}
}
```

## Testing

### Using cURL (HTTP)

**English Example**:
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

**Arabic Example**:
```bash
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "S456",
    "userId": "U456",
    "userRole": "employee",
    "message": "أريد إضافة سيرتي الذاتية"
  }'
```

### Using wscat (WebSocket)

**Install wscat**:
```bash
npm install -g wscat
```

**Connect**:
```bash
wscat -c "ws://localhost:8000/ws/S123/U123/employee"
```

**Send messages** (after connection):
```json
{"type":"user_message","message":"I want to add my resume","sessionId":"S123","userId":"U123","userRole":"employee"}
```

```json
{"type":"user_message","message":"أريد إضافة سيرتي الذاتية","sessionId":"S456","userId":"U456","userRole":"employee"}
```

### Using Python WebSocket Client

```python
import asyncio
import websockets
import json

async def test_agent():
    uri = "ws://localhost:8000/ws/S123/U123/employee"
    
    async with websockets.connect(uri) as websocket:
        # Send message
        message = {
            "type": "user_message",
            "message": "I want to add my resume",
            "sessionId": "S123",
            "userId": "U123",
            "userRole": "employee"
        }
        await websocket.send(json.dumps(message))
        
        # Receive responses
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(f"Received: {data['type']}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data['type'] == 'final_response':
                break

asyncio.run(test_agent())
```

## Example Conversations

### Add Resume (English)

**User**: "I want to add my resume"

**Agent**: 
1. Opens ticket
2. Asks for full name
3. Asks for job title
4. Asks for email
5. Asks for phone
6. Creates resume
7. Asks for confirmation
8. Closes ticket

### Add Resume (Arabic)

**User**: "أريد إضافة سيرتي الذاتية"

**Agent**:
1. يفتح تذكرة
2. يسأل عن الاسم الكامل
3. يسأل عن المسمى الوظيفي
4. يسأل عن البريد الإلكتروني
5. يسأل عن رقم الهاتف
6. ينشئ السيرة الذاتية
7. يسأل عن التأكيد
8. يغلق التذكرة

### Q&A Example

**User**: "What is Qiwa?"

**Agent**: "Qiwa is a comprehensive platform by the Ministry of Human Resources and Social Development in Saudi Arabia..."

## Event Schemas

### Chat Message Event

```json
{
  "type": "chat_message",
  "sessionId": "S123",
  "role": "assistant",
  "message": "What is your full name?",
  "timestamp": "2025-11-11T17:32:00Z"
}
```

### Process Update Event

```json
{
  "type": "process_update",
  "sessionId": "S123",
  "steps": [
    {
      "id": "open_ticket",
      "title": "Open ticket",
      "status": "done",
      "meta": {"ticketId": "T123"}
    },
    {
      "id": "gather_info",
      "title": "Gather required info",
      "status": "in_progress",
      "meta": {"fields": ["full_name"]}
    }
  ],
  "timestamp": "2025-11-11T17:32:05Z"
}
```

### Ticket Update Event

```json
{
  "type": "ticket_update",
  "sessionId": "S123",
  "ticket": {
    "ticketId": "T123",
    "type": "resume_add",
    "status": "open",
    "createdAt": "2025-11-11T17:32:00Z"
  },
  "timestamp": "2025-11-11T17:32:00Z"
}
```

### Final Response Event

```json
{
  "type": "final_response",
  "sessionId": "S123",
  "status": "success",
  "message": "Resume added successfully and ticket closed.",
  "ticketId": "T123",
  "timestamp": "2025-11-11T17:35:00Z"
}
```

## Logging

All logs are written to `/backend/Agents/logs/` in JSONL format:

- **chat_logs.jsonl**: All chat messages
- **actions.jsonl**: Tool executions
- **errors.jsonl**: Errors and exceptions
- **llm.jsonl**: LLM API calls with latency and token usage

View logs:
```bash
# View recent chat logs
tail -f logs/chat_logs.jsonl | jq

# View actions
tail -f logs/actions.jsonl | jq

# View errors
tail -f logs/errors.jsonl | jq
```

## Future Enhancements

### Local LLM Integration

To use local models (Ollama/LlamaCpp):

1. Set in `.env`:
   ```
   USE_LOCAL_LLM=true
   ```

2. Uncomment and implement local LLM code in `utils/llm_wrapper.py`

3. Install Ollama and pull a model:
   ```bash
   ollama pull llama2
   ```

### RAG Integration

To replace keyword matching with vector search:

1. Install vector database dependencies:
   ```bash
   pip install chromadb langchain-community
   ```

2. Implement vector store in `tools/shared/knowledge_tool.py`

3. Embed FAQ data and create vector index

### Backend API Integration

To connect to actual backend:

1. Update `config/settings.py` with backend URL

2. Replace simulated API calls in tools with real HTTP requests

3. Add authentication headers and error handling

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the correct directory:
```bash
cd /path/to/backend/Agents
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### OpenAI API Errors

- Verify your API key is correct in `.env`
- Check your OpenAI account has available credits
- Ensure you're not hitting rate limits

### WebSocket Connection Issues

- Verify the server is running on the correct port
- Check firewall settings
- Test with HTTP endpoint first

## Support

For issues or questions, please contact the development team or refer to the project documentation.

## License

Internal use only - Qiwa Platform Team


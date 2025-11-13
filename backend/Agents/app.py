"""
FastAPI application with WebSocket support for the Qiwa Agent System.
Provides real-time communication for agent interactions.
"""

import json
import os
import tempfile
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from openai import OpenAI
from routers.real_employee_router import RealEmployeeRouter
from config.settings import HOST, PORT, OPENAI_API_KEY, LOG_PATH
from storage.resume_storage import resume_storage
from storage.ticket_storage import ticket_storage

# Pydantic models for event schemas

class ChatMessageEvent(BaseModel):
    """Chat message event schema."""
    type: str = "chat_message"
    sessionId: str
    role: str
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class ProcessStep(BaseModel):
    """Process step schema."""
    id: str
    title: str
    status: str
    meta: Dict[str, Any] = Field(default_factory=dict)

class ProcessUpdateEvent(BaseModel):
    """Process update event schema."""
    type: str = "process_update"
    sessionId: str
    steps: List[ProcessStep]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class TicketData(BaseModel):
    """Ticket data schema."""
    ticketId: str
    type: str
    status: str
    createdAt: Optional[str] = None
    closedAt: Optional[str] = None

class TicketUpdateEvent(BaseModel):
    """Ticket update event schema."""
    type: str = "ticket_update"
    sessionId: str
    ticket: TicketData
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

class FinalResponseEvent(BaseModel):
    """Final response event schema."""
    type: str = "final_response"
    sessionId: str
    status: str
    message: str
    ticketId: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

# HTTP Request/Response models

class MessageRequest(BaseModel):
    """HTTP message request schema."""
    sessionId: str
    userId: str
    userRole: str
    message: str

class MessageResponse(BaseModel):
    """HTTP message response schema."""
    status: str
    sessionId: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    finalResponse: Optional[Dict[str, Any]] = None

# Initialize FastAPI app
app = FastAPI(
    title="Qiwa Agent System",
    description="AI-powered customer service agent for Qiwa platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize routers
employee_router = RealEmployeeRouter()  # NOW USING REAL AI AGENT!

# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, sessionId: str, websocket: WebSocket):
        """Accept and store WebSocket connection."""
        await websocket.accept()
        self.active_connections[sessionId] = websocket
    
    def disconnect(self, sessionId: str):
        """Remove WebSocket connection."""
        if sessionId in self.active_connections:
            del self.active_connections[sessionId]
    
    async def send_message(self, sessionId: str, message: dict):
        """Send message to specific session."""
        if sessionId in self.active_connections:
            websocket = self.active_connections[sessionId]
            await websocket.send_json(message)
    
    async def send_text(self, sessionId: str, text: str):
        """Send text to specific session."""
        if sessionId in self.active_connections:
            websocket = self.active_connections[sessionId]
            await websocket.send_text(text)

manager = ConnectionManager()

# Startup: Initialize mock user in Supabase
@app.on_event("startup")
async def startup_event():
    """Initialize mock user in Supabase on startup."""
    from config.settings import MOCK_USER_ID, MOCK_USER_NAME, MOCK_USER_PHONE, MOCK_USER_TYPE, MOCK_USER_ESTABLISHMENT_ID
    
    try:
        from database.supabase_storage import supabase_user_profile_storage
        # Create/update mock user profile with user type
        supabase_user_profile_storage.create_or_update_profile(
            userId=MOCK_USER_ID,
            full_name=MOCK_USER_NAME,
            phone=MOCK_USER_PHONE,
            user_type=MOCK_USER_TYPE,
            establishment_id=MOCK_USER_ESTABLISHMENT_ID if MOCK_USER_TYPE == "business_owner" else None
        )
        print(f"✅ Mock user initialized: {MOCK_USER_NAME} ({MOCK_USER_TYPE}) ({MOCK_USER_ID[:8]}...)")
    except Exception as e:
        print(f"⚠️ Mock user initialization failed (non-critical): {e}")

# Routes

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Qiwa Agent System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.websocket("/ws/{sessionId}/{userId}/{userRole}")
async def websocket_endpoint(
    websocket: WebSocket,
    sessionId: str,
    userId: str,
    userRole: str
):
    """
    WebSocket endpoint for real-time agent communication.
    
    Args:
        websocket: WebSocket connection
        sessionId: Session identifier
        userId: User identifier
        userRole: User role (employee, business_owner, service_provider)
    """
    await manager.connect(sessionId, websocket)
    
    # Create send function for this session
    async def ws_send_fn(event_dict: dict):
        """Send event to WebSocket."""
        await manager.send_message(sessionId, event_dict)
    
    try:
        # Send welcome message
        await ws_send_fn({
            "type": "chat_message",
            "sessionId": sessionId,
            "role": "system",
            "message": "Connected to Qiwa Agent. How can I help you today?",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                # Parse message
                message_data = json.loads(data)
                
                message_type = message_data.get("type", "user_message")
                message = message_data.get("message", "")
                
                if not message:
                    await ws_send_fn({
                        "type": "chat_message",
                        "sessionId": sessionId,
                        "role": "system",
                        "message": "Empty message received",
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    })
                    continue
                
                # Route to appropriate handler based on userRole
                if userRole == "employee":
                    # Use sync send function wrapper
                    def sync_ws_send(event_dict):
                        # We need to create a task for async send
                        import asyncio
                        asyncio.create_task(ws_send_fn(event_dict))
                    
                    result = employee_router.handle_message(
                        sessionId=sessionId,
                        userId=userId,
                        userRole=userRole,
                        message=message,
                        ws_send_fn=sync_ws_send
                    )
                else:
                    # TODO: Implement other user role routers
                    await ws_send_fn({
                        "type": "chat_message",
                        "sessionId": sessionId,
                        "role": "system",
                        "message": f"User role '{userRole}' is not yet supported",
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    })
            
            except json.JSONDecodeError:
                await ws_send_fn({
                    "type": "chat_message",
                    "sessionId": sessionId,
                    "role": "system",
                    "message": "Invalid JSON message",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            
            except Exception as e:
                await ws_send_fn({
                    "type": "chat_message",
                    "sessionId": sessionId,
                    "role": "system",
                    "message": f"Error processing message: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
    
    except WebSocketDisconnect:
        manager.disconnect(sessionId)
        print(f"Client {sessionId} disconnected")
    
    except Exception as e:
        print(f"WebSocket error for {sessionId}: {e}")
        manager.disconnect(sessionId)

@app.post("/agent/message", response_model=MessageResponse)
async def http_message_endpoint(request: MessageRequest):
    """
    HTTP fallback endpoint for agent communication.
    Useful for testing without WebSocket.
    
    Args:
        request: Message request
        
    Returns:
        Message response with final result
    """
    try:
        # Store messages and final response
        messages = []
        final_response = None
        
        def http_send_fn(event_dict: dict):
            """Collect events instead of sending via WebSocket."""
            nonlocal messages, final_response
            
            if event_dict.get("type") == "chat_message":
                messages.append({
                    "role": event_dict.get("role"),
                    "message": event_dict.get("message"),
                    "timestamp": event_dict.get("timestamp")
                })
            elif event_dict.get("type") == "final_response":
                final_response = event_dict
        
        # Route to appropriate handler
        if request.userRole == "employee":
            result = employee_router.handle_message(
                sessionId=request.sessionId,
                userId=request.userId,
                userRole=request.userRole,
                message=request.message,
                ws_send_fn=http_send_fn
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"User role '{request.userRole}' is not yet supported"
            )
        
        return MessageResponse(
            status=result.get("status", "success"),
            sessionId=request.sessionId,
            messages=messages,
            finalResponse=final_response
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{sessionId}")
async def get_session_state(sessionId: str):
    """
    Get current session state (for debugging).
    
    Args:
        sessionId: Session identifier
        
    Returns:
        Session state
    """
    state = employee_router.get_session_state(sessionId)
    
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Remove ws_send_fn from response (not serializable)
    response_state = {k: v for k, v in state.items() if k != "ws_send_fn"}
    
    return response_state

@app.delete("/session/{sessionId}")
async def clear_session(sessionId: str):
    """
    Clear session state.
    
    Args:
        sessionId: Session identifier
        
    Returns:
        Success message
    """
    employee_router.clear_session(sessionId)
    manager.disconnect(sessionId)
    
    return {"status": "success", "message": f"Session {sessionId} cleared"}

@app.get("/resumes/{userId}")
async def get_user_resumes(userId: str):
    """
    Get all resumes for a user.
    
    Args:
        userId: User identifier
        
    Returns:
        List of resumes
    """
    try:
        resumes = resume_storage.get_all_resumes(userId)
        return {
            "status": "success",
            "userId": userId,
            "resumes": resumes,
            "count": len(resumes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resume/{userId}/{resumeId}")
async def get_single_resume(userId: str, resumeId: str):
    """
    Get a specific resume.
    
    Args:
        userId: User identifier
        resumeId: Resume identifier
        
    Returns:
        Resume data
    """
    try:
        resume = resume_storage.get_resume(userId, resumeId)
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return {
            "status": "success",
            "resume": resume
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tickets/{userId}")
async def get_user_tickets(userId: str):
    """
    Get all tickets for a user.
    
    Args:
        userId: User identifier
        
    Returns:
        List of tickets
    """
    try:
        tickets = ticket_storage.get_all_tickets(userId)
        return {
            "status": "success",
            "userId": userId,
            "tickets": tickets,
            "count": len(tickets)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# NEW DATA ENDPOINTS (Contracts, Certificates, Permits, Reminders)
# ============================================================================

from storage.contract_storage import contract_storage
from storage.certificate_storage import certificate_storage
from storage.work_permit_storage import work_permit_storage
from storage.reminder_storage import reminder_storage

@app.get("/contracts/{userId}")
async def get_user_contracts(userId: str):
    """Get all contracts for a user."""
    try:
        contracts = contract_storage.get_all_contracts(userId)
        return {
            "status": "success",
            "userId": userId,
            "contracts": contracts,
            "count": len(contracts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/certificates/{userId}")
async def get_user_certificates(userId: str):
    """Get all certificates for a user."""
    try:
        certificates = certificate_storage.get_all_certificates(userId)
        return {
            "status": "success",
            "userId": userId,
            "certificates": certificates,
            "count": len(certificates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/permits/{establishmentId}")
async def get_establishment_permits(establishmentId: str):
    """Get all work permits for an establishment."""
    try:
        permits = work_permit_storage.get_all_permits(establishmentId)
        return {
            "status": "success",
            "establishmentId": establishmentId,
            "permits": permits,
            "count": len(permits)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reminders/{userId}")
async def get_user_reminders(userId: str):
    """Get all pending reminders for a user."""
    try:
        reminders = reminder_storage.get_pending_reminders(userId)
        return {
            "status": "success",
            "userId": userId,
            "reminders": reminders,
            "count": len(reminders)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# VOICE API ENDPOINTS
# ============================================================================

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio using OpenAI Whisper API.
    
    Args:
        audio: Audio file (webm, mp3, wav, etc.)
        
    Returns:
        JSON with transcribed text and language
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Call Whisper API for transcription
        with open(temp_file_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ar",  # Arabic
                response_format="text"
            )
        
        # Cleanup temp file
        os.unlink(temp_file_path)
        
        return {
            "text": transcript,
            "language": "ar",
            "success": True
        }
    except Exception as e:
        # Cleanup on error
        try:
            os.unlink(temp_file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.get("/api/audio/{filename}")
async def serve_audio(filename: str):
    """
    Serve generated TTS audio files.
    
    Args:
        filename: Audio file name
        
    Returns:
        Audio file as MP3
    """
    audio_dir = LOG_PATH / "audio"
    audio_path = audio_dir / filename
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )


"""
Router for employee interactions using the REAL AI agent.
The LLM makes intelligent decisions about which tools to use.
"""

from typing import Dict, Any, Callable
from agents.real_agent import create_real_agent
from memory.conversation_memory import get_user_memory, add_message
from utils.logger import log_chat, log_error
from datetime import datetime
import json
from openai import OpenAI
from config.settings import OPENAI_API_KEY, LOG_PATH

# Import Supabase logging and user tracking
try:
    from database.supabase_storage import (
        supabase_conversation_storage,
        supabase_user_behavior_storage,
        supabase_process_step_storage,
        supabase_user_profile_storage
    )
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase logging not available: {e}")
    SUPABASE_AVAILABLE = False

# Global state store for sessions
session_states: Dict[str, Dict[str, Any]] = {}
session_agents: Dict[str, Any] = {}

class RealEmployeeRouter:
    """Router for employee user interactions using real AI agent."""
    
    def __init__(self):
        """Initialize the RealEmployeeRouter."""
        pass
    
    def handle_message(
        self,
        sessionId: str,
        userId: str,
        userRole: str,
        message: str,
        ws_send_fn: Callable
    ) -> Dict[str, Any]:
        """
        Handle an incoming message from an employee user.
        
        Args:
            sessionId: Session identifier
            userId: User identifier
            userRole: User role (should be 'employee')
            message: User message content
            ws_send_fn: Callback function to send WebSocket events
            
        Returns:
            Dictionary with processing result
        """
        try:
            # Log the user message (JSON logs)
            log_chat(
                sessionId=sessionId,
                userId=userId,
                userRole=userRole,
                role="user",
                message=message
            )
            
            # LOG TO SUPABASE: User message
            if SUPABASE_AVAILABLE:
                try:
                    supabase_conversation_storage.log_message(userId, "user", message)
                except Exception as e:
                    print(f"⚠️ Supabase conversation logging failed: {e}")
            
            # Send user message via WebSocket
            ws_send_fn({
                "type": "chat_message",
                "sessionId": sessionId,
                "role": "user",
                "message": message,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            
            # Load conversation memory
            memory = get_user_memory(sessionId, userId)
            
            # Add current message to memory
            add_message(sessionId, "user", message)
            
            # Get or create agent for this session
            if sessionId not in session_agents:
                # LOAD USER PROFILE to get user_type
                user_type = "employee"  # Default
                establishment_id = None
                
                if SUPABASE_AVAILABLE:
                    try:
                        profile = supabase_user_profile_storage.get_profile(userId)
                        if profile:
                            user_type = profile.get("user_type", "employee")
                            establishment_id = profile.get("establishment_id")
                            print(f"✓ Loaded user profile: {user_type}")
                        else:
                            # Create profile if doesn't exist
                            supabase_user_profile_storage.create_or_update_profile(
                                userId=userId,
                                full_name=None,
                                phone=None,
                                user_type="employee"  # Default to employee
                            )
                    except Exception as e:
                        print(f"⚠️ User profile loading failed: {e}")
                
                # Create a function to get context for this session
                def get_context():
                    return session_states.get(sessionId, {})
                
                # CREATE AGENT with user_type and establishment_id
                session_agents[sessionId] = create_real_agent(userId, sessionId, user_type, establishment_id, get_context)
                
                # Load last accessed resume from persistent storage
                from storage.resume_storage import resume_storage
                last_resume_id = resume_storage.get_last_accessed_resume(userId)
                
                # Load pending reminders
                pending_reminders = []
                if SUPABASE_AVAILABLE:
                    try:
                        from storage.reminder_storage import reminder_storage
                        reminders = reminder_storage.get_pending_reminders(userId)
                        pending_reminders = reminders
                    except Exception as e:
                        print(f"⚠️ Reminder loading failed: {e}")
                
                session_states[sessionId] = {
                    "chat_history": [],
                    "current_ticket": None,
                    "last_resume_id": last_resume_id,  # Load from persistent storage!
                    "pending_reminders": pending_reminders,
                    "user_type": user_type,
                    "establishment_id": establishment_id
                }
                
                if last_resume_id:
                    print(f"✓ Restored resume context for {userId}: {last_resume_id}")
                if pending_reminders:
                    print(f"✓ Loaded {len(pending_reminders)} pending reminders")
            
            agent = session_agents[sessionId]
            state = session_states[sessionId]
            
            # Convert memory to chat history format
            chat_history = []
            for msg in memory[-10:]:  # Last 10 messages for context
                if msg["role"] == "user":
                    chat_history.append(("human", msg["content"]))
                elif msg["role"] == "assistant":
                    chat_history.append(("ai", msg["content"]))
            
            # Add system context about last resume if available
            if state.get("last_resume_id"):
                # Inject as SYSTEM message at the start so LLM sees it as context
                chat_history.insert(0, (
                    "system",
                    f"IMPORTANT CONTEXT: The user's most recently accessed resume is {state['last_resume_id']}. "
                    f"If the user says 'my resume', 'the resume', 'edit my CV', 'change the name', or similar phrases "
                    f"WITHOUT specifying a resume ID, automatically use {state['last_resume_id']}. "
                    f"Do NOT ask for the resume ID if it's obvious they mean their recent resume."
                ))
                print(f"💡 Injected resume context into chat history: {state['last_resume_id']}")
            
            # Run the agent - THE LLM DECIDES WHAT TO DO!
            result = agent.invoke({
                "input": message,
                "chat_history": chat_history
            })
            
            # Extract the response
            response = result.get("output", "عذراً، حدث خطأ في المعالجة.")
            
            # Log intermediate steps (tool calls)
            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                steps_info = []
                for action, observation in intermediate_steps:
                    steps_info.append({
                        "tool": action.tool,
                        "input": str(action.tool_input),
                        "output": str(observation)
                    })
                    
                    # Track last resume ID if a resume tool was used
                    if action.tool in ["add_resume", "edit_resume", "delete_resume"]:
                        try:
                            obs_dict = json.loads(observation) if isinstance(observation, str) else observation
                            if "resumeId" in obs_dict:
                                resume_id = obs_dict["resumeId"]
                                state["last_resume_id"] = resume_id
                                
                                # Persist to storage for future sessions
                                from storage.resume_storage import resume_storage
                                resume_storage.set_last_accessed_resume(userId, resume_id)
                                
                                print(f"✓ Tracked & persisted last resume ID: {resume_id}")
                        except:
                            pass
                
                # Send process update showing what the agent did
                process_steps = [
                    {
                        "id": f"step_{i}",
                        "title": step["tool"],
                        "status": "done",
                        "meta": {"input": step["input"][:100]}  # Truncate long inputs
                    }
                    for i, step in enumerate(steps_info)
                ]
                
                ws_send_fn({
                    "type": "process_update",
                    "sessionId": sessionId,
                    "steps": process_steps,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                
                # LOG TO SUPABASE: Process steps
                if SUPABASE_AVAILABLE:
                    try:
                        for step in process_steps:
                            supabase_process_step_storage.log_process_step(
                                userId=userId,
                                sessionId=sessionId,
                                step_id=step["id"],
                                step_title=step["title"],
                                step_status=step["status"],
                                step_meta=step.get("meta")
                            )
                    except Exception as e:
                        print(f"⚠️ Process step logging failed: {e}")
            
            # Send agent's response
            ws_send_fn({
                "type": "chat_message",
                "sessionId": sessionId,
                "role": "assistant",
                "message": response,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            
            # Save assistant message to memory
            add_message(sessionId, "assistant", response)
            
            # Log the assistant response (JSON logs)
            log_chat(
                sessionId=sessionId,
                userId=userId,
                userRole=userRole,
                role="assistant",
                message=response
            )
            
            # LOG TO SUPABASE: Assistant message
            if SUPABASE_AVAILABLE:
                try:
                    supabase_conversation_storage.log_message(userId, "assistant", response)
                except Exception as e:
                    print(f"⚠️ Supabase conversation logging failed: {e}")
            
            # GENERATE TTS AUDIO: Convert agent response to speech
            try:
                openai_client = OpenAI(api_key=OPENAI_API_KEY)
                
                # Generate speech from text
                audio_response = openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",  # Neutral voice for Arabic
                    input=response,
                    response_format="mp3"
                )
                
                # Save audio file
                audio_filename = f"tts_{sessionId}_{int(datetime.utcnow().timestamp() * 1000)}.mp3"
                audio_dir = LOG_PATH / "audio"
                audio_dir.mkdir(parents=True, exist_ok=True)
                audio_path = audio_dir / audio_filename
                
                audio_response.stream_to_file(str(audio_path))
                
                # Send audio URL via WebSocket
                ws_send_fn({
                    "type": "audio_response",
                    "sessionId": sessionId,
                    "audioUrl": f"/api/audio/{audio_filename}",
                    "text": response,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                
                print(f"✓ TTS audio generated: {audio_filename}")
                
            except Exception as e:
                # Non-critical: Text response already sent
                print(f"⚠️ TTS generation failed (non-critical): {e}")
            
            # UPDATE USER BEHAVIOR: Detect intent based on tools used
            if SUPABASE_AVAILABLE:
                try:
                    tools_used = [step[0].tool for step in intermediate_steps] if intermediate_steps else []
                    
                    # Simple intent detection based on tools
                    if any("resume" in tool.lower() for tool in tools_used):
                        intent = "service"  # Resume management service
                    elif any("ticket" in tool.lower() for tool in tools_used):
                        intent = "support"  # Support ticket
                    elif any("knowledge" in tool.lower() or "answer" in tool.lower() for tool in tools_used):
                        intent = "inquiry"  # Q&A inquiry
                    else:
                        intent = "support"  # Default to support
                    
                    supabase_user_behavior_storage.update_behavior(
                        userId=userId,
                        last_message=message[:500],  # Truncate to 500 chars
                        intent=intent,
                        predicted_need=" | ".join(tools_used) if tools_used else "محادثة عامة"
                    )
                except Exception as e:
                    print(f"⚠️ User behavior update failed: {e}")
            
            return {
                "status": "success",
                "response": response,
                "tools_used": [step[0].tool for step in intermediate_steps] if intermediate_steps else []
            }
            
        except Exception as e:
            error_msg = str(e)
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole=userRole,
                tool="RealEmployeeRouter.handle_message",
                error=error_msg,
                error_type=type(e).__name__
            )
            
            # Send error message
            ws_send_fn({
                "type": "chat_message",
                "sessionId": sessionId,
                "role": "assistant",
                "message": f"عذراً، حدث خطأ: {error_msg}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            
            return {
                "status": "error",
                "error": error_msg
            }
    
    def clear_session(self, sessionId: str):
        """Clear session state and agent."""
        if sessionId in session_agents:
            del session_agents[sessionId]
        if sessionId in session_states:
            del session_states[sessionId]


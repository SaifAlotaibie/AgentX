"""
Employee router for handling employee-specific requests.
Manages conversation state and invokes the employee agent.
"""

from typing import Dict, Any, Callable
from agents.employee_agent import create_employee_agent
from agents.base_agent import AgentState
from memory.conversation_memory import get_user_memory, add_message
from utils.logger import log_chat
from utils.language_detector import detect_language

# Global state store for sessions
# In production, this should be replaced with Redis or similar
session_states: Dict[str, Dict[str, Any]] = {}

class EmployeeRouter:
    """Router for employee user interactions."""
    
    def __init__(self):
        """Initialize the EmployeeRouter."""
        self.agent_graph = create_employee_agent()
    
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
            # Log the user message
            log_chat(
                sessionId=sessionId,
                userId=userId,
                userRole=userRole,
                role="user",
                message=message
            )
            
            # Load conversation memory
            memory = get_user_memory(sessionId, userId)
            
            # Add current message to memory
            add_message(sessionId, "user", message)
            memory.append({"role": "user", "content": message})
            
            # Get or create session state
            if sessionId not in session_states:
                session_states[sessionId] = {
                    "sessionId": sessionId,
                    "userId": userId,
                    "userRole": userRole,
                    "messages": memory,
                    "ws_send_fn": ws_send_fn,
                    "current_step": "start",
                    "ticket_id": None,
                    "resume_data": {},
                    "process_steps": [],
                    "intent": None,
                    "language": None,
                    "missing_fields": [],
                    "waiting_for_confirmation": False,
                    "error": None
                }
            else:
                # Update existing state with new message
                session_states[sessionId]["messages"] = memory
                session_states[sessionId]["ws_send_fn"] = ws_send_fn
                
                # If we're gathering info, extract data from message
                if session_states[sessionId].get("current_step") == "gather_info":
                    self._extract_data_from_message(session_states[sessionId], message)
                
                # If we're waiting for confirmation, check the message
                if session_states[sessionId].get("waiting_for_confirmation"):
                    session_states[sessionId]["waiting_for_confirmation"] = False
            
            # Get current state
            state: AgentState = session_states[sessionId]
            
            # Only invoke agent graph if we're starting new or not in middle of gathering
            current_step = state.get("current_step")
            
            # If we're gathering info and have a missing field, don't re-run the graph
            # Just emit a message asking for the next field
            if current_step == "gather_info" and state.get("missing_fields"):
                # Process the user's response and ask for next field
                missing_fields = state.get("missing_fields", [])
                if missing_fields:
                    field = missing_fields[0]
                    field_questions = {
                        "full_name": "ما هو اسمك الكامل؟",
                        "job_title": "ما هو المسمى الوظيفي الذي تريده؟",
                        "contact.email": "ما هو بريدك الإلكتروني؟",
                        "contact.phone": "ما هو رقم هاتفك؟"
                    }
                    # Don't emit again - it was already asked
                    # Just wait for user response
                    session_states[sessionId] = state
                    return {"status": "waiting_for_input", "state": state}
            
            # Invoke the agent graph only when needed
            # Set recursion limit to prevent infinite loops
            config = {"recursion_limit": 50}
            result_state = self.agent_graph.invoke(state, config=config)
            
            # Update session state
            session_states[sessionId] = result_state
            
            # Save assistant messages to memory
            # (already handled by emit functions, but we track state)
            
            return {
                "status": "success",
                "sessionId": sessionId,
                "current_step": result_state.get("current_step", "complete")
            }
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            
            # Send error message
            ws_send_fn({
                "type": "chat_message",
                "sessionId": sessionId,
                "role": "assistant",
                "message": "Sorry, an error occurred while processing your request.",
                "timestamp": ""
            })
            
            ws_send_fn({
                "type": "final_response",
                "sessionId": sessionId,
                "status": "error",
                "message": error_msg,
                "timestamp": ""
            })
            
            return {
                "status": "error",
                "sessionId": sessionId,
                "error": error_msg
            }
    
    def _extract_data_from_message(self, state: Dict[str, Any], message: str) -> None:
        """
        Extract resume data from user message based on missing fields.
        
        Args:
            state: Current session state
            message: User message
        """
        missing_fields = state.get("missing_fields", [])
        resume_data = state.get("resume_data", {})
        
        if not missing_fields:
            return
        
        # Get the first missing field
        field = missing_fields[0]
        
        # Extract data based on field
        if field == "full_name":
            resume_data["full_name"] = message.strip()
        elif field == "job_title":
            resume_data["job_title"] = message.strip()
        elif field == "contact.email":
            if "contact" not in resume_data:
                resume_data["contact"] = {}
            resume_data["contact"]["email"] = message.strip()
        elif field == "contact.phone":
            if "contact" not in resume_data:
                resume_data["contact"] = {}
            resume_data["contact"]["phone"] = message.strip()
        elif field == "section_to_edit":
            resume_data["section_to_edit"] = message.strip()
        elif field == "new_value":
            resume_data["new_value"] = message.strip()
        elif field == "confirmation":
            resume_data["confirmation"] = message.strip()
        
        # Remove this field from missing fields
        state["missing_fields"] = [f for f in missing_fields if f != field]
        state["resume_data"] = resume_data
    
    def clear_session(self, sessionId: str) -> None:
        """
        Clear session state.
        
        Args:
            sessionId: Session identifier
        """
        if sessionId in session_states:
            del session_states[sessionId]
    
    def get_session_state(self, sessionId: str) -> Dict[str, Any]:
        """
        Get current session state.
        
        Args:
            sessionId: Session identifier
            
        Returns:
            Session state dictionary or empty dict if not found
        """
        return session_states.get(sessionId, {})


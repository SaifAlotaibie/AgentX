"""
Base agent definition with state structure for LangGraph.
Defines the state and base classes used by all agents.
"""

from typing import TypedDict, List, Dict, Any, Callable, Optional
from datetime import datetime

class AgentState(TypedDict, total=False):
    """
    State structure for the agent graph.
    
    Attributes:
        messages: List of conversation messages
        current_step: Current processing step
        ticket_id: ID of the opened ticket (for resume operations)
        resume_data: Collected resume data
        process_steps: List of process steps for checklist
        ws_send_fn: WebSocket send function for real-time updates
        sessionId: Session identifier
        userId: User identifier
        userRole: User role (employee, business_owner, service_provider)
        intent: Detected intent (resume_add, resume_edit, resume_delete, qa)
        language: Detected language (ar, en)
        missing_fields: List of fields still needed for resume
        waiting_for_confirmation: Boolean indicating if waiting for user confirmation
        error: Error message if any
    """
    messages: List[Dict[str, str]]
    current_step: str
    ticket_id: str
    resume_data: Dict[str, Any]
    process_steps: List[Dict[str, Any]]
    ws_send_fn: Callable
    sessionId: str
    userId: str
    userRole: str
    intent: str
    language: str
    missing_fields: List[str]
    waiting_for_confirmation: bool
    error: Optional[str]

def create_process_steps(intent: str, language: str = "en") -> List[Dict[str, Any]]:
    """
    Create initial process steps based on intent.
    
    Args:
        intent: User intent (resume_add, resume_edit, resume_delete, qa)
        language: Language for step titles
        
    Returns:
        List of process step dictionaries
    """
    if language == "ar":
        if intent in ["resume_add", "resume_edit", "resume_delete"]:
            return [
                {"id": "open_ticket", "title": "فتح تذكرة", "status": "pending", "meta": {}},
                {"id": "gather_info", "title": "جمع المعلومات المطلوبة", "status": "pending", "meta": {}},
                {"id": "apply_change", "title": "تطبيق التغيير", "status": "pending", "meta": {}},
                {"id": "notify_user", "title": "إشعار المستخدم", "status": "pending", "meta": {}},
                {"id": "confirm_close", "title": "تأكيد المستخدم لإغلاق التذكرة", "status": "pending", "meta": {}}
            ]
    else:  # English
        if intent in ["resume_add", "resume_edit", "resume_delete"]:
            return [
                {"id": "open_ticket", "title": "Open ticket", "status": "pending", "meta": {}},
                {"id": "gather_info", "title": "Gather required info", "status": "pending", "meta": {}},
                {"id": "apply_change", "title": "Apply change to resume", "status": "pending", "meta": {}},
                {"id": "notify_user", "title": "Notify user", "status": "pending", "meta": {}},
                {"id": "confirm_close", "title": "User confirmation to close ticket", "status": "pending", "meta": {}}
            ]
    
    # For Q&A, no process steps needed
    return []

def update_step_status(
    steps: List[Dict[str, Any]],
    step_id: str,
    status: str,
    meta: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Update the status of a specific step.
    
    Args:
        steps: List of process steps
        step_id: ID of the step to update
        status: New status (pending, in_progress, done, failed)
        meta: Optional metadata to add to the step
        
    Returns:
        Updated list of steps
    """
    for step in steps:
        if step["id"] == step_id:
            step["status"] = status
            if meta:
                step["meta"].update(meta)
            break
    
    return steps

def emit_process_update(state: AgentState) -> None:
    """
    Emit a process update event via WebSocket.
    
    Args:
        state: Current agent state
    """
    if state.get("ws_send_fn") and state.get("process_steps"):
        event = {
            "type": "process_update",
            "sessionId": state.get("sessionId", ""),
            "steps": state.get("process_steps", []),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        state["ws_send_fn"](event)

def emit_chat_message(state: AgentState, role: str, message: str) -> None:
    """
    Emit a chat message event via WebSocket.
    
    Args:
        state: Current agent state
        role: Message role (user, assistant, system)
        message: Message content
    """
    if state.get("ws_send_fn"):
        event = {
            "type": "chat_message",
            "sessionId": state.get("sessionId", ""),
            "role": role,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        state["ws_send_fn"](event)

def emit_ticket_update(state: AgentState, ticket_data: Dict[str, Any]) -> None:
    """
    Emit a ticket update event via WebSocket.
    
    Args:
        state: Current agent state
        ticket_data: Ticket information
    """
    if state.get("ws_send_fn"):
        event = {
            "type": "ticket_update",
            "sessionId": state.get("sessionId", ""),
            "ticket": ticket_data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        state["ws_send_fn"](event)

def emit_final_response(
    state: AgentState,
    status: str,
    message: str,
    ticket_id: Optional[str] = None
) -> None:
    """
    Emit a final response event via WebSocket.
    
    Args:
        state: Current agent state
        status: Status (success, error, etc.)
        message: Final message
        ticket_id: Optional ticket ID
    """
    if state.get("ws_send_fn"):
        event = {
            "type": "final_response",
            "sessionId": state.get("sessionId", ""),
            "status": status,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if ticket_id:
            event["ticketId"] = ticket_id
        
        state["ws_send_fn"](event)


"""
Employee agent implementation using LangGraph.
Handles resume management and Q&A for employee users.
ALL RESPONSES IN ARABIC ONLY.
"""

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from agents.base_agent import (
    AgentState,
    create_process_steps,
    update_step_status,
    emit_process_update,
    emit_chat_message,
    emit_ticket_update,
    emit_final_response
)
from tools.shared.ticket_tool import TicketTool
from tools.employee.resume_tool import ResumeTool
from tools.shared.knowledge_tool import KnowledgeTool
from utils.language_detector import detect_language, extract_intent, is_confirmation
from utils.logger import log_chat
from config.settings import FORCE_ARABIC

# Initialize tools
ticket_tool = TicketTool()
resume_tool = ResumeTool()
knowledge_tool = KnowledgeTool()

def classify_intent_node(state: AgentState) -> AgentState:
    """
    Classify user intent from the message.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with intent and language
    """
    messages = state.get("messages", [])
    
    if messages:
        last_message = messages[-1]["content"]
        
        # Detect language
        language = detect_language(last_message)
        state["language"] = "ar" if FORCE_ARABIC else language  # Force Arabic
        
        # Extract intent
        intent = extract_intent(last_message, language)
        state["intent"] = intent
        
        # Create process steps if needed (Arabic only)
        if intent in ["resume_add", "resume_edit", "resume_delete"]:
            state["process_steps"] = create_process_steps(intent, "ar")
            state["resume_data"] = {}
            state["missing_fields"] = []
        
        state["current_step"] = "classify_intent"
    
    return state

def open_ticket_node(state: AgentState) -> AgentState:
    """
    Open a support ticket for resume operations.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with ticket information
    """
    intent = state.get("intent", "")
    
    # Update step status
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "open_ticket",
        "in_progress"
    )
    emit_process_update(state)
    
    # Ticket descriptions in Arabic
    descriptions = {
        "resume_add": "إضافة سيرة ذاتية جديدة",
        "resume_edit": "تعديل السيرة الذاتية",
        "resume_delete": "حذف السيرة الذاتية"
    }
    opening_message = "سأقوم بفتح تذكرة وسأساعدك خطوة بخطوة..."
    
    # Emit message
    emit_chat_message(state, "assistant", opening_message)
    
    # Open ticket
    ticket_result = ticket_tool.open_ticket(
        userId=state.get("userId", ""),
        ticket_type=intent,
        description=descriptions.get(intent, "عملية على السيرة الذاتية"),
        sessionId=state.get("sessionId", "")
    )
    
    state["ticket_id"] = ticket_result["ticketId"]
    
    # Update step status to done
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "open_ticket",
        "done",
        {"ticketId": ticket_result["ticketId"]}
    )
    emit_process_update(state)
    emit_ticket_update(state, ticket_result)
    
    state["current_step"] = "open_ticket"
    
    return state

def gather_info_node(state: AgentState) -> AgentState:
    """
    Gather required information from the user (Arabic only).
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with collected information
    """
    intent = state.get("intent", "")
    messages = state.get("messages", [])
    
    # Update step status
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "gather_info",
        "in_progress"
    )
    emit_process_update(state)
    
    # Define required fields based on intent
    if intent == "resume_add":
        required_fields = ["full_name", "job_title", "contact.email", "contact.phone"]
    elif intent == "resume_edit":
        required_fields = ["section_to_edit", "new_value"]
    elif intent == "resume_delete":
        required_fields = ["confirmation"]
    else:
        required_fields = []
    
    # Check what we already have
    resume_data = state.get("resume_data", {})
    missing_fields = []
    
    for field in required_fields:
        if "." in field:
            # Nested field
            parent, child = field.split(".")
            if parent not in resume_data or not resume_data[parent].get(child):
                missing_fields.append(field)
        else:
            if field not in resume_data or not resume_data[field]:
                missing_fields.append(field)
    
    # If we have missing fields, ask for the first one (Arabic only)
    if missing_fields:
        state["missing_fields"] = missing_fields
        field_to_ask = missing_fields[0]
        
        # Questions in Arabic only
        field_questions = {
            "full_name": "ما هو اسمك الكامل؟",
            "job_title": "ما هو المسمى الوظيفي الذي تريده؟",
            "contact.email": "ما هو بريدك الإلكتروني؟",
            "contact.phone": "ما هو رقم هاتفك؟",
            "section_to_edit": "أي قسم من السيرة الذاتية تريد تعديله؟ (مثل: المهارات، الخبرة، التعليم)",
            "new_value": "ما هي القيمة الجديدة؟",
            "confirmation": "هل أنت متأكد من حذف سيرتك الذاتية؟ (نعم/لا)"
        }
        
        question = field_questions.get(field_to_ask, f"يرجى تقديم {field_to_ask}")
        emit_chat_message(state, "assistant", question)
        
        # Update meta with collected fields
        collected_fields = [f for f in required_fields if f not in missing_fields]
        state["process_steps"] = update_step_status(
            state["process_steps"],
            "gather_info",
            "in_progress",
            {"fields": collected_fields}
        )
        emit_process_update(state)
    else:
        # All fields collected
        state["process_steps"] = update_step_status(
            state["process_steps"],
            "gather_info",
            "done",
            {"fields": required_fields}
        )
        emit_process_update(state)
    
    state["current_step"] = "gather_info"
    
    return state

def apply_change_node(state: AgentState) -> AgentState:
    """
    Apply the resume change using the ResumeTool.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with operation result
    """
    intent = state.get("intent", "")
    resume_data = state.get("resume_data", {})
    
    # Update step status
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "apply_change",
        "in_progress"
    )
    emit_process_update(state)
    
    try:
        if intent == "resume_add":
            result = resume_tool.add_resume(
                userId=state.get("userId", ""),
                resume_data=resume_data,
                sessionId=state.get("sessionId", "")
            )
            # Store resume ID for later access
            state["resume_id"] = result.get("resumeId")
            
        elif intent == "resume_edit":
            result = resume_tool.edit_resume(
                userId=state.get("userId", ""),
                resumeId=resume_data.get("resumeId", "R_DEFAULT"),
                changes=resume_data,
                sessionId=state.get("sessionId", "")
            )
        elif intent == "resume_delete":
            result = resume_tool.delete_resume(
                userId=state.get("userId", ""),
                resumeId=resume_data.get("resumeId", "R_DEFAULT"),
                sessionId=state.get("sessionId", "")
            )
        else:
            result = {"status": "error", "message": "نوع العملية غير معروف"}
        
        if result.get("status") == "success":
            state["process_steps"] = update_step_status(
                state["process_steps"],
                "apply_change",
                "done"
            )
        else:
            state["process_steps"] = update_step_status(
                state["process_steps"],
                "apply_change",
                "failed",
                {"error": result.get("message")}
            )
        
        emit_process_update(state)
        
    except Exception as e:
        state["error"] = str(e)
        state["process_steps"] = update_step_status(
            state["process_steps"],
            "apply_change",
            "failed",
            {"error": str(e)}
        )
        emit_process_update(state)
    
    state["current_step"] = "apply_change"
    
    return state

def notify_user_node(state: AgentState) -> AgentState:
    """
    Notify user of the operation result (Arabic only).
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    intent = state.get("intent", "")
    
    # Check if operation was successful
    error = state.get("error")
    
    if error:
        message = f"عذراً، حدث خطأ: {error}"
    else:
        messages_map = {
            "resume_add": "تم إضافة سيرتك الذاتية بنجاح! يمكنك الآن رؤيتها في لوحة التحكم.",
            "resume_edit": "تم تحديث سيرتك الذاتية بنجاح!",
            "resume_delete": "تم حذف سيرتك الذاتية بنجاح!"
        }
        
        message = messages_map.get(intent, "تمت العملية بنجاح!")
    
    emit_chat_message(state, "assistant", message)
    
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "notify_user",
        "done"
    )
    emit_process_update(state)
    
    state["current_step"] = "notify_user"
    
    return state

def confirm_close_node(state: AgentState) -> AgentState:
    """
    Ask user for confirmation to close the ticket (Arabic).
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    message = "هل أنت راضٍ عن النتيجة؟ هل تريد إغلاق التذكرة؟ (نعم/لا)"
    
    emit_chat_message(state, "assistant", message)
    
    state["waiting_for_confirmation"] = True
    state["current_step"] = "confirm_close"
    
    return state

def close_ticket_node(state: AgentState) -> AgentState:
    """
    Close the support ticket.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    # Close ticket
    ticket_result = ticket_tool.close_ticket(
        ticketId=state.get("ticket_id", ""),
        userId=state.get("userId", ""),
        sessionId=state.get("sessionId", "")
    )
    
    state["process_steps"] = update_step_status(
        state["process_steps"],
        "confirm_close",
        "done"
    )
    emit_process_update(state)
    emit_ticket_update(state, ticket_result)
    
    # Send final message
    message = "تم إغلاق التذكرة. شكراً لاستخدامك منصة قوى!"
    
    emit_final_response(state, "success", message, state.get("ticket_id"))
    
    state["current_step"] = "close_ticket"
    
    return state

def qa_node(state: AgentState) -> AgentState:
    """
    Handle Q&A using the KnowledgeTool (Arabic).
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    messages = state.get("messages", [])
    
    if messages:
        last_message = messages[-1]["content"]
        
        # Get answer from knowledge tool (force Arabic)
        result = knowledge_tool.answer_question(
            userId=state.get("userId", ""),
            query=last_message,
            language="ar",  # Force Arabic
            sessionId=state.get("sessionId", "")
        )
        
        answer = result.get("answer", "")
        
        # Send answer
        emit_chat_message(state, "assistant", answer)
        emit_final_response(state, "success", answer)
    
    state["current_step"] = "qa"
    
    return state

def route_after_classify(state: AgentState) -> Literal["open_ticket", "qa"]:
    """
    Route to appropriate node after intent classification.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    intent = state.get("intent", "qa")
    
    if intent in ["resume_add", "resume_edit", "resume_delete"]:
        return "open_ticket"
    else:
        return "qa"

def route_after_gather_info(state: AgentState) -> Literal["gather_info", "apply_change"]:
    """
    Route after gathering info - either continue gathering or apply change.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    missing_fields = state.get("missing_fields", [])
    
    if missing_fields:
        return "gather_info"
    else:
        return "apply_change"

def route_after_confirm(state: AgentState) -> Literal["close_ticket", "notify_user"]:
    """
    Route after confirmation - either close ticket or keep it open.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    messages = state.get("messages", [])
    
    if messages:
        last_message = messages[-1]["content"]
        if is_confirmation(last_message, "ar"):
            return "close_ticket"
    
    return "notify_user"

def create_employee_agent() -> StateGraph:
    """
    Create the employee agent graph.
    
    Returns:
        Compiled StateGraph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("open_ticket", open_ticket_node)
    workflow.add_node("gather_info", gather_info_node)
    workflow.add_node("apply_change", apply_change_node)
    workflow.add_node("notify_user", notify_user_node)
    workflow.add_node("confirm_close", confirm_close_node)
    workflow.add_node("close_ticket", close_ticket_node)
    workflow.add_node("qa", qa_node)
    
    # Set entry point
    workflow.set_entry_point("classify_intent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "classify_intent",
        route_after_classify,
        {
            "open_ticket": "open_ticket",
            "qa": "qa"
        }
    )
    
    # Resume flow edges
    workflow.add_edge("open_ticket", "gather_info")
    
    workflow.add_conditional_edges(
        "gather_info",
        route_after_gather_info,
        {
            "gather_info": "gather_info",
            "apply_change": "apply_change"
        }
    )
    
    workflow.add_edge("apply_change", "notify_user")
    workflow.add_edge("notify_user", "confirm_close")
    
    workflow.add_conditional_edges(
        "confirm_close",
        route_after_confirm,
        {
            "close_ticket": "close_ticket",
            "notify_user": "notify_user"
        }
    )
    
    workflow.add_edge("close_ticket", END)
    workflow.add_edge("qa", END)
    
    return workflow.compile()

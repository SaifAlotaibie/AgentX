"""
REAL AI Agent that uses LLM function calling to decide which tools to use.
The LLM makes intelligent decisions instead of following hardcoded rules.
"""

from typing import Dict, Any, List, Callable
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, FunctionMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import json
import time
from config.settings import OPENAI_API_KEY, MODEL_NAME, MODEL_TEMPERATURE, DEV_MODE_ALL_FEATURES
from tools.shared.ticket_tool import TicketTool
from tools.employee.resume_tool import ResumeTool
from tools.shared.knowledge_tool import KnowledgeTool
from utils.logger import log_action

# Import Supabase logging
try:
    from database.supabase_storage import supabase_tool_call_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase logging not available: {e}")
    SUPABASE_AVAILABLE = False

# Initialize tools
ticket_tool = TicketTool()
resume_tool = ResumeTool()
knowledge_tool = KnowledgeTool()

# Import new tools
from tools.employee.contract_tool import ContractTool
from tools.employee.certificate_tool import CertificateTool
from tools.business.work_permit_tool import WorkPermitTool
from tools.provider.reward_calculator_tool import RewardCalculatorTool
from tools.shared.reminder_tool import ReminderTool

contract_tool = ContractTool()
certificate_tool = CertificateTool()
work_permit_tool = WorkPermitTool()
reward_calculator_tool = RewardCalculatorTool()
reminder_tool = ReminderTool()


# Pydantic schemas for tool inputs
class OpenTicketInput(BaseModel):
    ticket_type: str = Field(description="Type of ticket: resume_add, resume_edit, resume_delete, or qa")
    description: str = Field(description="Description of the issue or request in Arabic")

class CloseTicketInput(BaseModel):
    ticket_id: str = Field(description="The ticket ID to close")

class AddResumeInput(BaseModel):
    full_name: str = Field(description="Full name of the person")
    job_title: str = Field(description="Desired job title")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")

class EditResumeInput(BaseModel):
    resume_id: str = Field(
        default="",  # Make it optional
        description="The resume ID to edit. If empty, use the user's most recent resume from context."
    )
    field_name: str = Field(description="Field to edit: full_name, job_title, email, or phone")
    new_value: str = Field(description="New value for the field")

class DeleteResumeInput(BaseModel):
    resume_id: str = Field(description="The resume ID to delete")

class AnswerQuestionInput(BaseModel):
    question: str = Field(description="The user's question in Arabic or English")

# NEW: Contract tool schemas
class ViewContractInput(BaseModel):
    pass  # No input needed

class RequestRenewalInput(BaseModel):
    contract_id: str = Field(description="Contract ID to renew")
    updated_salary: str = Field(default="", description="New salary if requesting increase")

# NEW: Certificate tool schemas
class RequestCertificateInput(BaseModel):
    purpose: str = Field(description="Purpose of certificate (visa, loan, new_job, etc)")
    certificate_type: str = Field(description="Type: salary or experience")

# NEW: Work Permit tool schemas  
class ViewPermitsInput(BaseModel):
    pass  # Uses establishment_id from user profile

class CheckExpiringPermitsInput(BaseModel):
    days_threshold: int = Field(default=30, description="Check permits expiring within N days")

class RenewPermitInput(BaseModel):
    permit_id: str = Field(description="Permit ID to renew")

# NEW: Reward Calculator schema
class CalculateRewardInput(BaseModel):
    start_date: str = Field(description="Employment start date (YYYY-MM-DD)")
    end_date: str = Field(description="Employment end date (YYYY-MM-DD)")
    monthly_salary: float = Field(description="Monthly salary in SAR")
    termination_type: str = Field(description="Type: resignation, contract_end, or termination")

# NEW: Reminder tool schemas
class GetRemindersInput(BaseModel):
    pass  # No input needed

class DismissReminderInput(BaseModel):
    reminder_id: str = Field(description="Reminder ID to dismiss")


def create_agent_tools(userId: str, sessionId: str, user_type: str = "employee", 
                       establishment_id: str = None, get_context_fn=None) -> List[StructuredTool]:
    """
    Create LangChain tools that the agent can use based on user type.
    
    Args:
        userId: User ID for tool calls
        sessionId: Session ID for logging
        user_type: User type (employee, business_owner, service_provider)
        establishment_id: Establishment ID (for business owners)
        get_context_fn: Function to get session context
        
    Returns:
        List of LangChain StructuredTool objects appropriate for user type
    """
    
    def open_ticket_fn(ticket_type: str, description: str) -> str:
        """Open a support ticket for the user."""
        result = ticket_tool.open_ticket(
            userId=userId,
            ticket_type=ticket_type,
            description=description,
            sessionId=sessionId
        )
        return f"تم فتح التذكرة: {result['ticketId']} - الحالة: {result['status']}"
    
    def close_ticket_fn(ticket_id: str) -> str:
        """Close an open support ticket."""
        result = ticket_tool.close_ticket(
            ticketId=ticket_id,
            userId=userId,
            sessionId=sessionId
        )
        return f"تم إغلاق التذكرة {ticket_id} بنجاح"
    
    def add_resume_fn(full_name: str, job_title: str, email: str, phone: str) -> str:
        """Add a new resume for the user."""
        resume_data = {
            "full_name": full_name,
            "job_title": job_title,
            "contact": {
                "email": email,
                "phone": phone
            }
        }
        
        result = resume_tool.add_resume(
            userId=userId,
            resume_data=resume_data,
            sessionId=sessionId
        )
        
        if result["status"] == "success":
            return f"تم إضافة السيرة الذاتية بنجاح! رقم السيرة: {result['resumeId']}"
        else:
            return f"خطأ في إضافة السيرة الذاتية: {result.get('message', 'خطأ غير معروف')}"
    
    def edit_resume_fn(resume_id: str, field_name: str, new_value: str) -> str:
        """Edit an existing resume."""
        # AUTO-FILL resume_id from context if not provided
        if not resume_id or resume_id.strip() == "":
            if get_context_fn:
                context = get_context_fn()
                resume_id = context.get("last_resume_id", "")
                if resume_id:
                    print(f"🔧 Auto-filled resume_id from context: {resume_id}")
                else:
                    return "خطأ: لم أتمكن من العثور على رقم السيرة الذاتية. يرجى تحديد رقم السيرة."
            else:
                return "خطأ: يرجى تحديد رقم السيرة الذاتية المراد تعديلها."
        
        changes = {field_name: new_value}
        
        result = resume_tool.edit_resume(
            userId=userId,
            resumeId=resume_id,
            changes=changes,
            sessionId=sessionId
        )
        
        if result["status"] == "success":
            return f"تم تحديث السيرة الذاتية {resume_id} بنجاح!"
        else:
            return f"خطأ في تحديث السيرة الذاتية: {result.get('message', 'خطأ غير معروف')}"
    
    def delete_resume_fn(resume_id: str) -> str:
        """Delete a resume."""
        # AUTO-FILL resume_id from context if not provided
        if not resume_id or resume_id.strip() == "":
            if get_context_fn:
                context = get_context_fn()
                resume_id = context.get("last_resume_id", "")
                if resume_id:
                    print(f"🔧 Auto-filled resume_id from context: {resume_id}")
                else:
                    return "خطأ: لم أتمكن من العثور على رقم السيرة الذاتية. يرجى تحديد رقم السيرة."
            else:
                return "خطأ: يرجى تحديد رقم السيرة الذاتية المراد حذفها."
        
        result = resume_tool.delete_resume(
            userId=userId,
            resumeId=resume_id,
            sessionId=sessionId
        )
        
        if result["status"] == "success":
            return f"تم حذف السيرة الذاتية {resume_id} بنجاح!"
        else:
            return f"خطأ في حذف السيرة الذاتية: {result.get('message', 'خطأ غير معروف')}"
    
    def answer_question_fn(question: str) -> str:
        """Answer questions about Qiwa services and employment."""
        result = knowledge_tool.answer_question(
            userId=userId,
            query=question,
            language="ar",
            sessionId=sessionId
        )
        return result.get("answer", "عذراً، لم أتمكن من العثور على إجابة.")
    
    # Create StructuredTool objects
    tools = [
        StructuredTool.from_function(
            func=open_ticket_fn,
            name="open_ticket",
            description="افتح تذكرة دعم عندما يريد المستخدم إضافة أو تعديل أو حذف سيرته الذاتية. مطلوب لأي عمليات على السير الذاتية.",
            args_schema=OpenTicketInput
        ),
        StructuredTool.from_function(
            func=close_ticket_fn,
            name="close_ticket",
            description="أغلق تذكرة الدعم بعد إكمال طلب المستخدم والتأكد من رضاه.",
            args_schema=CloseTicketInput
        ),
        StructuredTool.from_function(
            func=add_resume_fn,
            name="add_resume",
            description="أضف سيرة ذاتية جديدة للمستخدم. استخدم هذه الأداة فقط بعد جمع كل المعلومات المطلوبة من المستخدم (الاسم، المسمى الوظيفي، البريد، الهاتف).",
            args_schema=AddResumeInput
        ),
        StructuredTool.from_function(
            func=edit_resume_fn,
            name="edit_resume",
            description="عدل سيرة ذاتية موجودة. يجب معرفة رقم السيرة (resume_id) والحقل المراد تعديله.",
            args_schema=EditResumeInput
        ),
        StructuredTool.from_function(
            func=delete_resume_fn,
            name="delete_resume",
            description="احذف سيرة ذاتية. يجب معرفة رقم السيرة (resume_id).",
            args_schema=DeleteResumeInput
        ),
        StructuredTool.from_function(
            func=answer_question_fn,
            name="answer_question",
            description="أجب على أسئلة المستخدم حول خدمات قوى، أنظمة التوظيف، أو استفسارات عامة. استخدم هذا عندما لا يطلب المستخدم عمليات على السيرة الذاتية.",
            args_schema=AnswerQuestionInput
        )
    ]
    
    # Add user-type-specific tools (OR ALL if in dev mode)
    if user_type == "employee" or DEV_MODE_ALL_FEATURES:
        # Contract management tools
        def view_contract_fn() -> str:
            """View employee's contract."""
            result = contract_tool.view_contract(userId, sessionId)
            if result["status"] == "success":
                contract = result["contract"]["data"]
                return f"عقدك: الشركة: {contract.get('employer_name')}, الوظيفة: {contract.get('job_title')}, الراتب: {contract.get('salary')} ريال"
            return result["message"]
        
        def request_certificate_fn(purpose: str, certificate_type: str) -> str:
            """Request salary or experience certificate."""
            if certificate_type == "salary":
                result = certificate_tool.request_salary_certificate(userId, purpose, sessionId)
            else:
                result = certificate_tool.request_experience_letter(userId, purpose, sessionId)
            return result["message"]
        
        tools.extend([
            StructuredTool.from_function(
                func=view_contract_fn,
                name="view_contract",
                description="اعرض تفاصيل عقد العمل الحالي للموظف.",
                args_schema=ViewContractInput
            ),
            StructuredTool.from_function(
                func=request_certificate_fn,
                name="request_certificate",
                description="اطلب شهادة راتب أو خطاب خبرة للموظف. حدد الغرض (visa, loan, new_job) والنوع (salary أو experience).",
                args_schema=RequestCertificateInput
            )
        ])
    
    if user_type == "business_owner" or DEV_MODE_ALL_FEATURES:
        # Work permit management tools
        def view_permits_fn() -> str:
            """View all work permits."""
            result = work_permit_tool.view_permits(establishment_id or userId, sessionId)
            return f"لديك {result['count']} تصريح عمل"
        
        def check_expiring_permits_fn(days_threshold: int = 30) -> str:
            """Check expiring permits."""
            result = work_permit_tool.check_expiring_permits(establishment_id or userId, days_threshold, sessionId)
            if result['count'] > 0:
                expiring_names = [p['data']['employee_name'] for p in result['expiring_permits'][:3]]
                return f"⚠️ {result['count']} تصريح ينتهي قريباً: {', '.join(expiring_names)}"
            return "لا توجد تصاريح تنتهي قريباً"
        
        def renew_permit_fn(permit_id: str) -> str:
            """Renew a work permit."""
            result = work_permit_tool.renew_permit(establishment_id or userId, permit_id, sessionId)
            return result["message"]
        
        tools.extend([
            StructuredTool.from_function(
                func=view_permits_fn,
                name="view_permits",
                description="اعرض جميع تصاريح العمل للمنشأة.",
                args_schema=ViewPermitsInput
            ),
            StructuredTool.from_function(
                func=check_expiring_permits_fn,
                name="check_expiring_permits",
                description="تحقق من التصاريح التي تنتهي قريباً (خلال 30 يوم افتراضياً).",
                args_schema=CheckExpiringPermitsInput
            ),
            StructuredTool.from_function(
                func=renew_permit_fn,
                name="renew_permit",
                description="جدد تصريح عمل محدد.",
                args_schema=RenewPermitInput
            )
        ])
    
    if user_type == "service_provider" or DEV_MODE_ALL_FEATURES:
        # Reward calculator tool
        def calculate_reward_fn(start_date: str, end_date: str, monthly_salary: float, termination_type: str) -> str:
            """Calculate end of service reward."""
            result = reward_calculator_tool.calculate_reward(userId, start_date, end_date, monthly_salary, termination_type, sessionId)
            return f"مكافأة نهاية الخدمة: {result['reward_amount']:,.2f} ريال\n\n{result['explanation']}"
        
        tools.append(
            StructuredTool.from_function(
                func=calculate_reward_fn,
                name="calculate_reward",
                description="احسب مكافأة نهاية الخدمة حسب نظام العمل السعودي. تحتاج: تاريخ البداية، تاريخ النهاية، الراتب الشهري، نوع الإنهاء (resignation/contract_end/termination).",
                args_schema=CalculateRewardInput
            )
        )
    
    # Shared reminder tools for all users
    def get_reminders_fn() -> str:
        """Get pending reminders."""
        result = reminder_tool.get_pending_reminders(userId, sessionId)
        if result['count'] > 0:
            reminders_text = "\n".join([f"- {r['data']['message']}" for r in result['reminders'][:3]])
            return f"لديك {result['count']} تذكيرات:\n{reminders_text}"
        return "لا توجد تذكيرات معلقة"
    
    tools.append(
        StructuredTool.from_function(
            func=get_reminders_fn,
            name="get_reminders",
            description="احصل على التذكيرات المعلقة للمستخدم.",
            args_schema=GetRemindersInput
        )
    )
    
    return tools


class RealAgent:
    """AI Agent that uses LLM function calling to make decisions."""
    
    def __init__(self, userId: str, sessionId: str, user_type: str = "employee", 
                 establishment_id: str = None, get_context_fn=None):
        """
        Initialize the real agent.
        
        Args:
            userId: User ID
            sessionId: Session ID
            user_type: User type (employee, business_owner, service_provider)
            establishment_id: Establishment ID (for business owners)
            get_context_fn: Optional function to get session context
        """
        self.userId = userId
        self.sessionId = sessionId
        self.user_type = user_type
        self.establishment_id = establishment_id
        self.get_context_fn = get_context_fn
        
        # Initialize LLM with function calling
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=MODEL_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        
        # Get tools (with user type routing)
        self.tools = create_agent_tools(userId, sessionId, user_type, establishment_id, get_context_fn)
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # System prompt in Arabic (dynamic based on user type)
        if DEV_MODE_ALL_FEATURES:
            # Development mode: ALL features available
            self.system_prompt = """أنت مساعد ذكي لمنصة قوى (Qiwa) - منصة التوظيف السعودية.
🔧 وضع التطوير: جميع الميزات متاحة للاختبار!

مهامك الشاملة:
1. إدارة السير الذاتية (إضافة، تعديل، حذف) - تحتاج التعليم والخبرة إلزامياً!
2. عرض وإدارة عقود العمل
3. طلب شهادات الراتب وخطابات الخبرة
4. عرض وتجديد تصاريح العمل
5. حساب مكافأة نهاية الخدمة
6. عرض التذكيرات الاستباقية
7. الإجابة على الأسئلة حول خدمات قوى

قواعد مهمة:
- السيرة الذاتية تحتاج: الاسم، الوظيفة، البريد، الهاتف، التعليم (إلزامي)، الخبرة (إلزامي)
- عند طلب شهادة: اسأل عن الغرض (visa, loan, new_job) والنوع (salary أو experience)
- لحساب مكافأة نهاية الخدمة: اطلب تاريخ البداية، النهاية، الراتب، نوع الإنهاء
- تحدث بالعربية دائماً وكن مهذباً ومساعداً"""
        
        elif user_type == "employee":
            self.system_prompt = """أنت مساعد ذكي لمنصة قوى (Qiwa) - منصة التوظيف السعودية.
نوع المستخدم: موظف

مهامك:
1. إدارة السير الذاتية (إضافة، تعديل، حذف) - تحتاج التعليم والخبرة إلزامياً!
2. عرض وإدارة عقود العمل
3. طلب شهادات الراتب وخطابات الخبرة
4. الإجابة على الأسئلة حول خدمات قوى

قواعد مهمة:
- السيرة الذاتية تحتاج: الاسم، الوظيفة، البريد، الهاتف، التعليم (إلزامي)، الخبرة (إلزامي)
- عند طلب شهادة: اسأل عن الغرض (visa, loan, new_job)
- تحدث بالعربية دائماً وكن مهذباً"""
        
        elif user_type == "business_owner":
            self.system_prompt = """أنت مساعد ذكي لمنصة قوى (Qiwa) - منصة التوظيف السعودية.
نوع المستخدم: صاحب عمل

مهامك:
1. عرض تصاريح العمل للموظفين
2. التحقق من التصاريح التي تنتهي قريباً  
3. تجديد تصاريح العمل (فردي أو جماعي)
4. الإجابة على الأسئلة حول خدمات قوى

قواعد مهمة:
- تحقق بشكل دوري من التصاريح المنتهية
- اقترح التجديد الجماعي إذا كان هناك أكثر من تصريح ينتهي قريباً
- تحدث بالعربية دائماً وكن محترفاً"""
        
        elif user_type == "service_provider":
            self.system_prompt = """أنت مساعد ذكي لمنصة قوى (Qiwa) - منصة التوظيف السعودية.
نوع المستخدم: مقدم خدمة

مهامك:
1. حساب مكافأة نهاية الخدمة حسب نظام العمل السعودي
2. شرح كيفية الحساب بوضوح
3. الإجابة على الأسئلة حول خدمات قوى

قواعد مهمة:
- اطلب: تاريخ البداية، تاريخ النهاية، الراتب الشهري، نوع الإنهاء
- اشرح الحساب خطوة بخطوة
- تحدث بالعربية دائماً وكن دقيقاً"""
        
        else:
            self.system_prompt = """أنت مساعد ذكي لمنصة قوى (Qiwa) - منصة التوظيف السعودية.
تحدث بالعربية دائماً وكن مهذباً ومساعداً."""
    
    def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and make decisions.
        
        Args:
            input_dict: Dictionary with 'input' and optional 'chat_history'
            
        Returns:
            Dictionary with 'output' and 'intermediate_steps'
        """
        user_input = input_dict["input"]
        chat_history = input_dict.get("chat_history", [])
        
        # Build message history
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add chat history
        for role, content in chat_history:
            if role == "human":
                messages.append(HumanMessage(content=content))
            elif role == "ai":
                messages.append(AIMessage(content=content))
        
        # Add current user input
        messages.append(HumanMessage(content=user_input))
        
        # Track tool calls
        intermediate_steps = []
        max_iterations = 5
        
        for iteration in range(max_iterations):
            # Call LLM
            response = self.llm_with_tools.invoke(messages)
            
            # Add AI response to messages
            messages.append(response)
            
            # Check if LLM wants to call tools
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # Execute tool calls
                from langchain_core.messages import ToolMessage
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_input = tool_call["args"]
                    tool_call_id = tool_call["id"]
                    
                    # Find and execute the tool
                    tool = next((t for t in self.tools if t.name == tool_name), None)
                    if tool:
                        # Track execution time
                        start_time = time.time()
                        tool_success = True
                        tool_error = None
                        
                        try:
                            tool_output = tool.invoke(tool_input)
                            
                            # Track intermediate step
                            intermediate_steps.append((
                                type('Action', (), {'tool': tool_name, 'tool_input': tool_input})(),
                                tool_output
                            ))
                            
                            # Add tool result to messages with correct format
                            messages.append(ToolMessage(
                                tool_call_id=tool_call_id,
                                content=str(tool_output)
                            ))
                        except Exception as e:
                            tool_success = False
                            tool_error = str(e)
                            tool_output = f"خطأ في تنفيذ الأداة {tool_name}: {str(e)}"
                            
                            error_msg = tool_output
                            messages.append(ToolMessage(
                                tool_call_id=tool_call_id,
                                content=error_msg
                            ))
                        
                        # Calculate execution time
                        execution_time_ms = int((time.time() - start_time) * 1000)
                        
                        # LOG TO SUPABASE: Tool call with timing
                        if SUPABASE_AVAILABLE:
                            try:
                                supabase_tool_call_storage.log_tool_call(
                                    userId=self.userId,
                                    sessionId=self.sessionId,
                                    tool_name=tool_name,
                                    tool_input=tool_input,
                                    tool_output=str(tool_output),
                                    execution_time_ms=execution_time_ms,
                                    success=tool_success,
                                    error_message=tool_error
                                )
                            except Exception as log_error:
                                # Don't break if logging fails
                                print(f"⚠️ Tool call logging failed: {log_error}")
            else:
                # No tool calls, this is the final response
                return {
                    "output": response.content,
                    "intermediate_steps": intermediate_steps
                }
        
        # Max iterations reached
        return {
            "output": response.content if hasattr(response, 'content') else "عذراً، حدث خطأ في المعالجة.",
            "intermediate_steps": intermediate_steps
        }


def create_real_agent(userId: str, sessionId: str, user_type: str = "employee", 
                      establishment_id: str = None, get_context_fn=None) -> RealAgent:
    """
    Create a real AI agent with user-type-specific capabilities.
    
    Args:
        userId: User ID
        sessionId: Session ID
        user_type: User type (employee, business_owner, service_provider)
        establishment_id: Establishment ID (for business owners)
        get_context_fn: Optional function to get session context
        
    Returns:
        RealAgent instance
    """
    return RealAgent(userId, sessionId, user_type, establishment_id, get_context_fn)

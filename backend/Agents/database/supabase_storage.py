"""
Supabase storage classes for all database operations.
Mirrors the JSON storage system with database persistence.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import logging
import json
from database.supabase_client import supabase, safe_supabase_call

logger = logging.getLogger(__name__)


class SupabaseResumeStorage:
    """Manages resume storage in Supabase."""
    
    @safe_supabase_call
    def save_resume(self, userId: str, resumeId: str, resume_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Save a resume to Supabase.
        
        Args:
            userId: User ID (UUID string)
            resumeId: Resume ID
            resume_data: Resume content
            
        Returns:
            Saved resume data or None if failed
        """
        try:
            # Ensure userId is UUID format
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "resume_id": resumeId,
                "full_name": resume_data.get("full_name"),
                "job_title": resume_data.get("job_title"),
                "contact": json.dumps(resume_data.get("contact", {})),
                "education": json.dumps(resume_data.get("education", [])),
                "experience": json.dumps(resume_data.get("experience", [])),
                "skills": json.dumps(resume_data.get("skills", [])),
                "summary": resume_data.get("summary"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table('resumes').insert(data).execute()
            logger.info(f"✓ Resume saved to Supabase: {resumeId}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to save resume to Supabase: {e}")
            return None
    
    @safe_supabase_call
    def update_resume(self, userId: str, resumeId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a resume in Supabase."""
        try:
            # Prepare update data
            update_data = {"updated_at": datetime.utcnow().isoformat()}
            
            # Handle nested fields
            for key, value in changes.items():
                if isinstance(value, (dict, list)):
                    update_data[key] = json.dumps(value)
                else:
                    update_data[key] = value
            
            response = supabase.table('resumes').update(update_data).eq('resume_id', resumeId).execute()
            logger.info(f"✓ Resume updated in Supabase: {resumeId}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to update resume in Supabase: {e}")
            return None
    
    @safe_supabase_call
    def delete_resume(self, userId: str, resumeId: str) -> bool:
        """Delete a resume from Supabase."""
        try:
            response = supabase.table('resumes').delete().eq('resume_id', resumeId).execute()
            logger.info(f"✓ Resume deleted from Supabase: {resumeId}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete resume from Supabase: {e}")
            return False
    
    @safe_supabase_call
    def get_all_resumes(self, userId: str) -> List[Dict[str, Any]]:
        """Get all resumes for a user from Supabase."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            response = supabase.table('resumes').select('*').eq('user_id', user_uuid).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"✗ Failed to get resumes from Supabase: {e}")
            return []


class SupabaseTicketStorage:
    """Manages ticket storage in Supabase."""
    
    @safe_supabase_call
    def save_ticket(self, ticket: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Save a ticket to Supabase."""
        try:
            user_uuid = str(uuid.UUID(ticket["userId"])) if not is_valid_uuid(ticket["userId"]) else ticket["userId"]
            
            data = {
                "user_id": user_uuid,
                "ticket_id": ticket["ticketId"],
                "type": ticket["type"],
                "description": ticket.get("description", ""),
                "status": ticket["status"],
                "created_at": ticket.get("createdAt", datetime.utcnow().isoformat()),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table('tickets').insert(data).execute()
            logger.info(f"✓ Ticket saved to Supabase: {ticket['ticketId']}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to save ticket to Supabase: {e}")
            return None
    
    @safe_supabase_call
    def update_ticket(self, userId: str, ticketId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a ticket in Supabase."""
        try:
            update_data = {**changes, "updated_at": datetime.utcnow().isoformat()}
            
            if changes.get("status") == "closed":
                update_data["closed_at"] = datetime.utcnow().isoformat()
            
            response = supabase.table('tickets').update(update_data).eq('ticket_id', ticketId).execute()
            logger.info(f"✓ Ticket updated in Supabase: {ticketId}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to update ticket in Supabase: {e}")
            return None
    
    @safe_supabase_call
    def get_all_tickets(self, userId: str) -> List[Dict[str, Any]]:
        """Get all tickets for a user from Supabase."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            response = supabase.table('tickets').select('*').eq('user_id', user_uuid).order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"✗ Failed to get tickets from Supabase: {e}")
            return []


class SupabaseConversationStorage:
    """Manages conversation history in Supabase."""
    
    @safe_supabase_call
    def log_message(self, userId: str, role: str, content: str) -> Optional[Dict[str, Any]]:
        """
        Log a conversation message to Supabase.
        
        Args:
            userId: User ID
            role: "user" or "assistant"
            content: Message content
            
        Returns:
            Logged message data or None
        """
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "role": role,
                "content": content,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table('conversations').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to log message to Supabase: {e}")
            return None
    
    @safe_supabase_call
    def get_conversation_history(self, userId: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history for a user."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            response = supabase.table('conversations').select('*').eq('user_id', user_uuid).order('created_at', desc=True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"✗ Failed to get conversation history: {e}")
            return []


class SupabaseUserBehaviorStorage:
    """Manages user behavior tracking in Supabase."""
    
    @safe_supabase_call
    def update_behavior(self, userId: str, last_message: str, intent: str, predicted_need: str = "قيد التحليل") -> Optional[Dict[str, Any]]:
        """
        Update user behavior data.
        
        Args:
            userId: User ID
            last_message: Last message from user
            intent: Detected intent (service, complaint, inquiry, support)
            predicted_need: Predicted user need
            
        Returns:
            Updated behavior data or None
        """
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "last_message": last_message,
                "predicted_need": predicted_need,
                "intent": intent,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Upsert (insert or update)
            response = supabase.table('user_behavior').upsert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to update user behavior: {e}")
            return None
    
    @safe_supabase_call
    def get_behavior(self, userId: str) -> Optional[Dict[str, Any]]:
        """Get user behavior data."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            response = supabase.table('user_behavior').select('*').eq('user_id', user_uuid).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"✗ Failed to get user behavior: {e}")
            return None


class SupabaseToolCallStorage:
    """Manages tool call logging for analytics."""
    
    @safe_supabase_call
    def log_tool_call(self, userId: str, sessionId: str, tool_name: str, tool_input: Any, 
                     tool_output: str, execution_time_ms: int, success: bool = True, 
                     error_message: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Log a tool call to Supabase.
        
        Args:
            userId: User ID
            sessionId: Session ID
            tool_name: Name of the tool called
            tool_input: Tool input parameters
            tool_output: Tool output/result
            execution_time_ms: Execution time in milliseconds
            success: Whether the call succeeded
            error_message: Error message if failed
            
        Returns:
            Logged tool call data or None
        """
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "session_id": sessionId,
                "tool_name": tool_name,
                "tool_input": json.dumps(tool_input) if isinstance(tool_input, (dict, list)) else str(tool_input),
                "tool_output": str(tool_output)[:5000],  # Limit output size
                "execution_time_ms": execution_time_ms,
                "success": success,
                "error_message": error_message,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table('tool_calls').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to log tool call: {e}")
            return None


class SupabaseProcessStepStorage:
    """Manages process step tracking for live checklist."""
    
    @safe_supabase_call
    def log_process_step(self, userId: str, sessionId: str, step_id: str, step_title: str,
                        step_status: str, step_meta: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Log a process step to Supabase.
        
        Args:
            userId: User ID
            sessionId: Session ID
            step_id: Step identifier
            step_title: Step title
            step_status: Step status (pending, in_progress, done, failed)
            step_meta: Additional metadata
            
        Returns:
            Logged step data or None
        """
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "session_id": sessionId,
                "step_id": step_id,
                "step_title": step_title,
                "step_status": step_status,
                "step_meta": json.dumps(step_meta) if step_meta else None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table('process_steps').insert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to log process step: {e}")
            return None


class SupabaseUserProfileStorage:
    """Manages user profile storage."""
    
    @safe_supabase_call
    def create_or_update_profile(self, userId: str, full_name: Optional[str] = None, 
                                phone: Optional[str] = None, user_type: Optional[str] = None,
                                establishment_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Create or update user profile.
        
        Args:
            userId: User ID (UUID)
            full_name: User's full name
            phone: User's phone number
            user_type: User type (employee, business_owner, service_provider)
            establishment_id: Establishment ID (for business owners)
            
        Returns:
            Profile data or None
        """
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "full_name": full_name or "مستخدم قوى",
                "phone": phone,
                "user_type": user_type or "employee",
                "establishment_id": establishment_id,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Upsert profile
            response = supabase.table('user_profile').upsert(data).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"✗ Failed to create/update user profile: {e}")
            return None
    
    @safe_supabase_call
    def get_profile(self, userId: str) -> Optional[Dict[str, Any]]:
        """Get user profile."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            response = supabase.table('user_profile').select('*').eq('user_id', user_uuid).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"✗ Failed to get user profile: {e}")
            return None


# Utility function
def is_valid_uuid(val):
    """Check if string is valid UUID."""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


# Export singleton instances
# NEW: Contract Storage
class SupabaseContractStorage:
    """Manages contract storage in Supabase."""
    
    @safe_supabase_call
    def save_contract(self, userId: str, contractId: str, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Save a contract to Supabase."""
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            
            data = {
                "user_id": user_uuid,
                "contract_id": contractId,
                "employer_id": contract_data.get("employer_id"),
                "employer_name": contract_data.get("employer_name"),
                "job_title": contract_data.get("job_title"),
                "salary": contract_data.get("salary"),
                "start_date": contract_data.get("start_date"),
                "end_date": contract_data.get("end_date"),
                "status": contract_data.get("status", "active"),
                "renewal_history": json.dumps(contract_data.get("renewal_history", [])),
                "termination_reason": contract_data.get("termination_reason"),
                "termination_date": contract_data.get("termination_date")
            }
            
            response = supabase.table('contracts').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error saving contract: {e}")
            return None
    
    @safe_supabase_call
    def update_contract(self, userId: str, contractId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table('contracts').update(changes).eq('contract_id', contractId).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating contract: {e}")
            return None
    
    @safe_supabase_call
    def delete_contract(self, userId: str, contractId: str) -> bool:
        try:
            supabase.table('contracts').delete().eq('contract_id', contractId).execute()
            return True
        except Exception as e:
            return False


# NEW: Certificate Storage  
class SupabaseCertificateStorage:
    """Manages certificate storage in Supabase."""
    
    @safe_supabase_call
    def save_certificate(self, userId: str, certificateId: str, cert_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            data = {
                "user_id": user_uuid,
                "certificate_id": certificateId,
                "type": cert_data.get("type"),
                "purpose": cert_data.get("purpose"),
                "status": cert_data.get("status", "requested"),
                "employee_data": json.dumps(cert_data.get("employee_data", {}))
            }
            response = supabase.table('certificates').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error saving certificate: {e}")
            return None
    
    @safe_supabase_call
    def update_certificate(self, userId: str, certificateId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table('certificates').update(changes).eq('certificate_id', certificateId).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None


# NEW: Work Permit Storage
class SupabaseWorkPermitStorage:
    """Manages work permit storage in Supabase."""
    
    @safe_supabase_call
    def save_permit(self, establishmentId: str, permitId: str, permit_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            data = {
                "establishment_id": establishmentId,
                "permit_id": permitId,
                "employee_name": permit_data.get("employee_name"),
                "nationality": permit_data.get("nationality"),
                "job_title": permit_data.get("job_title"),
                "expiry_date": permit_data.get("expiry_date"),
                "status": permit_data.get("status", "active")
            }
            response = supabase.table('work_permits').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None
    
    @safe_supabase_call
    def update_permit(self, establishmentId: str, permitId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table('work_permits').update(changes).eq('permit_id', permitId).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None


# NEW: Reminder Storage
class SupabaseReminderStorage:
    """Manages reminder storage in Supabase."""
    
    @safe_supabase_call
    def save_reminder(self, userId: str, reminderId: str, reminder_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            user_uuid = str(uuid.UUID(userId)) if not is_valid_uuid(userId) else userId
            data = {
                "user_id": user_uuid,
                "reminder_id": reminderId,
                "reminder_type": reminder_data.get("reminder_type"),
                "message": reminder_data.get("message"),
                "trigger_date": reminder_data.get("trigger_date"),
                "status": reminder_data.get("status", "pending")
            }
            response = supabase.table('reminders').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None
    
    @safe_supabase_call
    def update_reminder(self, userId: str, reminderId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table('reminders').update(changes).eq('reminder_id', reminderId).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            return None


# Singleton instances
supabase_resume_storage = SupabaseResumeStorage()
supabase_ticket_storage = SupabaseTicketStorage()
supabase_conversation_storage = SupabaseConversationStorage()
supabase_user_behavior_storage = SupabaseUserBehaviorStorage()
supabase_tool_call_storage = SupabaseToolCallStorage()
supabase_process_step_storage = SupabaseProcessStepStorage()
supabase_user_profile_storage = SupabaseUserProfileStorage()
supabase_contract_storage = SupabaseContractStorage()
supabase_certificate_storage = SupabaseCertificateStorage()
supabase_work_permit_storage = SupabaseWorkPermitStorage()
supabase_reminder_storage = SupabaseReminderStorage()


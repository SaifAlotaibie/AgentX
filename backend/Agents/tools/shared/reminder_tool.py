"""
Reminder tool for proactive notifications.
"""

from typing import Dict, Any, List
from utils.logger import log_action, log_error
from storage.reminder_storage import reminder_storage


class ReminderTool:
    """Tool for managing proactive reminders."""
    
    def __init__(self):
        """Initialize the ReminderTool."""
        pass
    
    def get_pending_reminders(
        self,
        userId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Get all pending reminders for a user.
        """
        try:
            pending = reminder_storage.get_pending_reminders(userId)
            
            result = {
                "status": "success",
                "count": len(pending),
                "reminders": pending,
                "message": f"لديك {len(pending)} تذكير معلق" if len(pending) > 0 else "لا توجد تذكيرات معلقة"
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.get_pending_reminders",
                inputs={"userId": userId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.get_pending_reminders",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def dismiss_reminder(
        self,
        userId: str,
        reminderId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Dismiss a reminder (user ignores it).
        """
        try:
            success = reminder_storage.mark_as_dismissed(userId, reminderId)
            
            if success:
                result = {
                    "status": "success",
                    "reminderId": reminderId,
                    "message": "تم تجاهل التذكير"
                }
            else:
                result = {
                    "status": "not_found",
                    "message": "التذكير غير موجود"
                }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.dismiss_reminder",
                inputs={"userId": userId, "reminderId": reminderId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.dismiss_reminder",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def action_reminder(
        self,
        userId: str,
        reminderId: str,
        action: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Take action on a reminder (user responds).
        """
        try:
            action_data = {
                "action": action,
                "timestamp": log_action.__module__  # Placeholder
            }
            
            success = reminder_storage.mark_as_actioned(userId, reminderId, action_data)
            
            if success:
                result = {
                    "status": "success",
                    "reminderId": reminderId,
                    "action": action,
                    "message": f"تم تنفيذ الإجراء: {action}"
                }
            else:
                result = {
                    "status": "not_found",
                    "message": "التذكير غير موجود"
                }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.action_reminder",
                inputs={"userId": userId, "reminderId": reminderId, "action": action},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ReminderTool.action_reminder",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


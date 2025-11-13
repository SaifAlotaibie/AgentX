"""
Resume management tool for CRUD operations on employee resumes.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.logger import log_action, log_error
from storage.resume_storage import resume_storage

class ResumeTool:
    """Tool for managing employee resumes."""
    
    def __init__(self):
        """Initialize the ResumeTool."""
        pass
    
    def validate_resume_data(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate resume data and return validation result.
        
        Args:
            resume_data: Resume data to validate
            
        Returns:
            Dictionary with validation result and missing fields
        """
        required_fields = ["full_name", "job_title", "contact", "education", "experience"]
        missing_fields = []
        
        for field in required_fields:
            if field not in resume_data or not resume_data[field]:
                missing_fields.append(field)
        
        # Check contact subfields
        if "contact" in resume_data and resume_data["contact"]:
            contact = resume_data["contact"]
            if not contact.get("email"):
                missing_fields.append("contact.email")
            if not contact.get("phone"):
                missing_fields.append("contact.phone")
        
        # Validate education structure
        if "education" in resume_data and resume_data["education"]:
            if not isinstance(resume_data["education"], list) or len(resume_data["education"]) == 0:
                missing_fields.append("education (يجب أن تكون قائمة غير فارغة)")
            else:
                for i, edu in enumerate(resume_data["education"]):
                    if not edu.get("school"):
                        missing_fields.append(f"education[{i}].school")
                    if not edu.get("degree"):
                        missing_fields.append(f"education[{i}].degree")
                    if not edu.get("year"):
                        missing_fields.append(f"education[{i}].year")
        
        # Validate experience structure
        if "experience" in resume_data and resume_data["experience"]:
            if not isinstance(resume_data["experience"], list) or len(resume_data["experience"]) == 0:
                missing_fields.append("experience (يجب أن تكون قائمة غير فارغة)")
            else:
                for i, exp in enumerate(resume_data["experience"]):
                    if not exp.get("company"):
                        missing_fields.append(f"experience[{i}].company")
                    if not exp.get("role"):
                        missing_fields.append(f"experience[{i}].role")
                    if not exp.get("start_date"):
                        missing_fields.append(f"experience[{i}].start_date")
        
        is_valid = len(missing_fields) == 0
        
        return {
            "is_valid": is_valid,
            "missing_fields": missing_fields
        }
    
    def add_resume(
        self,
        userId: str,
        resume_data: Dict[str, Any],
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Add a new resume for an employee.
        
        Args:
            userId: User identifier
            resume_data: Resume data including:
                - full_name (required)
                - job_title (required)
                - contact.email (required)
                - contact.phone (required)
                - summary (optional)
                - skills (optional list)
                - education (optional list)
                - experience (optional list)
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Validate resume data
            validation = self.validate_resume_data(resume_data)
            
            if not validation["is_valid"]:
                result = {
                    "status": "error",
                    "message": "Missing required fields",
                    "missing_fields": validation["missing_fields"]
                }
                
                log_action(
                    sessionId=sessionId,
                    userId=userId,
                    userRole="employee",
                    tool="ResumeTool.add_resume",
                    inputs={"userId": userId, "resume_data": resume_data},
                    outputs=result
                )
                
                return result
            
            # Generate unique resume ID
            resume_id = f"R{str(uuid.uuid4())[:8].upper()}"
            
            # Create timestamp
            created_at = datetime.utcnow().isoformat() + "Z"
            
            # Save to storage
            saved_resume = resume_storage.save_resume(userId, resume_id, resume_data)
            
            result = {
                "status": "success",
                "resumeId": resume_id,
                "message": "تم إضافة السيرة الذاتية بنجاح",
                "createdAt": saved_resume["createdAt"],
                "resume": saved_resume
            }
            
            # Log the action
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.add_resume",
                inputs={
                    "userId": userId,
                    "resume_data": resume_data
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.add_resume",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def edit_resume(
        self,
        userId: str,
        resumeId: str,
        changes: Dict[str, Any],
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Edit an existing resume.
        
        Args:
            userId: User identifier
            resumeId: Resume identifier
            changes: Dictionary of fields to update
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Create timestamp
            updated_at = datetime.utcnow().isoformat() + "Z"
            
            # Update in storage
            updated_resume = resume_storage.update_resume(userId, resumeId, changes)
            
            if updated_resume:
                result = {
                    "status": "success",
                    "resumeId": resumeId,
                    "message": "تم تحديث السيرة الذاتية بنجاح",
                    "updatedFields": list(changes.keys()),
                    "updatedAt": updated_resume["updatedAt"]
                }
            else:
                result = {
                    "status": "error",
                    "message": "السيرة الذاتية غير موجودة"
                }
            
            # Log the action
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.edit_resume",
                inputs={
                    "userId": userId,
                    "resumeId": resumeId,
                    "changes": changes
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.edit_resume",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def delete_resume(
        self,
        userId: str,
        resumeId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Delete a resume.
        
        Args:
            userId: User identifier
            resumeId: Resume identifier
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Create timestamp
            deleted_at = datetime.utcnow().isoformat() + "Z"
            
            # Delete from storage
            deleted = resume_storage.delete_resume(userId, resumeId)
            
            if deleted:
                result = {
                    "status": "success",
                    "resumeId": resumeId,
                    "message": "تم حذف السيرة الذاتية بنجاح",
                    "deletedAt": deleted_at
                }
            else:
                result = {
                    "status": "error",
                    "message": "السيرة الذاتية غير موجودة"
                }
            
            # Log the action
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.delete_resume",
                inputs={
                    "userId": userId,
                    "resumeId": resumeId
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ResumeTool.delete_resume",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


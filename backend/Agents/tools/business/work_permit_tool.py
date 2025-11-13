"""
Work permit management tool for business owners.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from utils.logger import log_action, log_error
from storage.work_permit_storage import work_permit_storage


class WorkPermitTool:
    """Tool for managing work permits for employees."""
    
    def __init__(self):
        """Initialize the WorkPermitTool."""
        pass
    
    def view_permits(
        self,
        establishmentId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        View all work permits for an establishment.
        """
        try:
            permits = work_permit_storage.get_all_permits(establishmentId)
            
            result = {
                "status": "success",
                "count": len(permits),
                "permits": permits,
                "message": f"لديك {len(permits)} تصريح عمل"
            }
            
            log_action(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.view_permits",
                inputs={"establishmentId": establishmentId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.view_permits",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def check_expiring_permits(
        self,
        establishmentId: str,
        days_threshold: int = 30,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Check for permits expiring soon.
        """
        try:
            expiring_permits = work_permit_storage.check_expiring_permits(establishmentId, days_threshold)
            
            result = {
                "status": "success",
                "count": len(expiring_permits),
                "expiring_permits": expiring_permits,
                "message": f"لديك {len(expiring_permits)} تصريح ينتهي خلال {days_threshold} يوم"
            }
            
            log_action(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.check_expiring_permits",
                inputs={"establishmentId": establishmentId, "days_threshold": days_threshold},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.check_expiring_permits",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def renew_permit(
        self,
        establishmentId: str,
        permitId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Renew a single work permit.
        """
        try:
            # Simulate renewal
            permit = work_permit_storage.get_permit(establishmentId, permitId)
            
            if permit:
                # Extend expiry by 1 year
                current_expiry = datetime.fromisoformat(permit["data"]["expiry_date"].replace('Z', ''))
                new_expiry = current_expiry + timedelta(days=365)
                
                updated = work_permit_storage.update_permit(establishmentId, permitId, {
                    "expiry_date": new_expiry.isoformat() + "Z",
                    "status": "active"
                })
                
                result = {
                    "status": "success",
                    "permitId": permitId,
                    "message": f"تم تجديد التصريح {permitId} حتى {new_expiry.date()}",
                    "permit": updated
                }
            else:
                result = {
                    "status": "not_found",
                    "message": "التصريح غير موجود"
                }
            
            log_action(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.renew_permit",
                inputs={"establishmentId": establishmentId, "permitId": permitId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.renew_permit",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def bulk_renew_permits(
        self,
        establishmentId: str,
        permitIds: List[str],
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Renew multiple work permits at once.
        """
        try:
            renewed = []
            failed = []
            
            for permit_id in permitIds:
                result = self.renew_permit(establishmentId, permit_id, sessionId)
                if result["status"] == "success":
                    renewed.append(permit_id)
                else:
                    failed.append(permit_id)
            
            result = {
                "status": "success",
                "renewed_count": len(renewed),
                "failed_count": len(failed),
                "renewed": renewed,
                "failed": failed,
                "message": f"تم تجديد {len(renewed)} تصريح من {len(permitIds)}"
            }
            
            log_action(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.bulk_renew_permits",
                inputs={"establishmentId": establishmentId, "permitIds": permitIds},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=establishmentId,
                userRole="business_owner",
                tool="WorkPermitTool.bulk_renew_permits",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


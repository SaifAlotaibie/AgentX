"""
Employment contract management tool for employees.
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from utils.logger import log_action, log_error
from storage.contract_storage import contract_storage


class ContractTool:
    """Tool for managing employment contracts."""
    
    def __init__(self):
        """Initialize the ContractTool."""
        pass
    
    def view_contract(
        self,
        userId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        View user's employment contract.
        """
        try:
            contracts = contract_storage.get_all_contracts(userId)
            
            if not contracts:
                result = {
                    "status": "not_found",
                    "message": "لا توجد عقود مسجلة"
                }
            else:
                # Get most recent active contract
                active_contracts = [c for c in contracts if c["data"].get("status") == "active"]
                
                if active_contracts:
                    contract = active_contracts[0]
                    result = {
                        "status": "success",
                        "contract": contract,
                        "message": "تم العثور على العقد"
                    }
                else:
                    result = {
                        "status": "no_active",
                        "message": "لا توجد عقود نشطة",
                        "contracts": contracts
                    }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.view_contract",
                inputs={"userId": userId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.view_contract",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def request_renewal(
        self,
        userId: str,
        contractId: str,
        updated_terms: Dict[str, Any],
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Request contract renewal with updated terms.
        """
        try:
            # This would open a ticket in real system
            result = {
                "status": "success",
                "message": "تم إرسال طلب تجديد العقد بنجاح",
                "contractId": contractId,
                "ticketId": f"T{str(uuid.uuid4())[:8].upper()}",
                "updated_terms": updated_terms
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.request_renewal",
                inputs={"userId": userId, "contractId": contractId, "updated_terms": updated_terms},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.request_renewal",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def request_termination(
        self,
        userId: str,
        contractId: str,
        reason: str,
        effective_date: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Request contract termination.
        """
        try:
            result = {
                "status": "success",
                "message": "تم إرسال طلب إنهاء العقد",
                "contractId": contractId,
                "ticketId": f"T{str(uuid.uuid4())[:8].upper()}",
                "reason": reason,
                "effective_date": effective_date
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.request_termination",
                inputs={"userId": userId, "contractId": contractId, "reason": reason},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="ContractTool.request_termination",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


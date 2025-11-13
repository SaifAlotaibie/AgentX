"""
Certificate request tool for employees (salary certificate, experience letter).
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from utils.logger import log_action, log_error
from storage.certificate_storage import certificate_storage


class CertificateTool:
    """Tool for requesting salary certificates and experience letters."""
    
    def __init__(self):
        """Initialize the CertificateTool."""
        pass
    
    def request_salary_certificate(
        self,
        userId: str,
        purpose: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Request a salary certificate.
        """
        try:
            certificate_id = f"CERT{str(uuid.uuid4())[:8].upper()}"
            
            cert_data = {
                "type": "salary",
                "purpose": purpose,
                "status": "requested",
                "request_date": datetime.utcnow().isoformat() + "Z"
            }
            
            saved_cert = certificate_storage.save_certificate(userId, certificate_id, cert_data)
            
            result = {
                "status": "success",
                "certificateId": certificate_id,
                "message": f"تم استلام طلب شهادة الراتب للغرض: {purpose}. سيتم معالجته خلال 24 ساعة.",
                "certificate": saved_cert
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.request_salary_certificate",
                inputs={"userId": userId, "purpose": purpose},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.request_salary_certificate",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def request_experience_letter(
        self,
        userId: str,
        purpose: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Request an experience letter.
        """
        try:
            certificate_id = f"CERT{str(uuid.uuid4())[:8].upper()}"
            
            cert_data = {
                "type": "experience",
                "purpose": purpose,
                "status": "requested",
                "request_date": datetime.utcnow().isoformat() + "Z"
            }
            
            saved_cert = certificate_storage.save_certificate(userId, certificate_id, cert_data)
            
            result = {
                "status": "success",
                "certificateId": certificate_id,
                "message": f"تم استلام طلب خطاب الخبرة للغرض: {purpose}. سيتم معالجته خلال 24 ساعة.",
                "certificate": saved_cert
            }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.request_experience_letter",
                inputs={"userId": userId, "purpose": purpose},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.request_experience_letter",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def check_certificate_status(
        self,
        userId: str,
        certificateId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Check the status of a certificate request.
        """
        try:
            certificate = certificate_storage.get_certificate(userId, certificateId)
            
            if certificate:
                result = {
                    "status": "found",
                    "certificate": certificate,
                    "message": f"حالة الشهادة: {certificate['data']['status']}"
                }
            else:
                result = {
                    "status": "not_found",
                    "message": "الشهادة غير موجودة"
                }
            
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.check_certificate_status",
                inputs={"userId": userId, "certificateId": certificateId},
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="CertificateTool.check_certificate_status",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


"""
Certificate storage system using DUAL STORAGE: JSON files + Supabase.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config.settings import LOG_PATH

# Create certificates directory
CERTIFICATES_PATH = LOG_PATH / "certificates"
CERTIFICATES_PATH.mkdir(parents=True, exist_ok=True)

# Import Supabase storage
try:
    from database.supabase_storage import supabase_certificate_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available for certificates: {e}")
    SUPABASE_AVAILABLE = False


class CertificateStorage:
    """Manages certificate storage in JSON files + Supabase."""
    
    def __init__(self):
        """Initialize storage."""
        CERTIFICATES_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's certificates."""
        return CERTIFICATES_PATH / f"{userId}_certificates.json"
    
    def _load_user_certificates(self, userId: str) -> List[Dict[str, Any]]:
        """Load all certificates for a user."""
        file_path = self._get_user_file(userId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_user_certificates(self, userId: str, certificates: List[Dict[str, Any]]):
        """Save all certificates for a user."""
        file_path = self._get_user_file(userId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(certificates, f, ensure_ascii=False, indent=2)
    
    def save_certificate(self, userId: str, certificateId: str, cert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a certificate request."""
        certificates = self._load_user_certificates(userId)
        
        # Create certificate object
        certificate = {
            "certificateId": certificateId,
            "userId": userId,
            "data": cert_data,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # PRIMARY: Save to JSON
        certificates.append(certificate)
        self._save_user_certificates(userId, certificates)
        
        # SECONDARY: Save to Supabase
        if SUPABASE_AVAILABLE:
            try:
                supabase_certificate_storage.save_certificate(userId, certificateId, cert_data)
            except Exception as e:
                print(f"⚠️ Supabase save failed (non-critical): {e}")
        
        return certificate
    
    def get_certificate(self, userId: str, certificateId: str) -> Optional[Dict[str, Any]]:
        """Get a specific certificate."""
        certificates = self._load_user_certificates(userId)
        
        for certificate in certificates:
            if certificate["certificateId"] == certificateId:
                return certificate
        
        return None
    
    def get_all_certificates(self, userId: str) -> List[Dict[str, Any]]:
        """Get all certificates for a user."""
        return self._load_user_certificates(userId)
    
    def update_certificate(self, userId: str, certificateId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a certificate."""
        certificates = self._load_user_certificates(userId)
        
        for i, certificate in enumerate(certificates):
            if certificate["certificateId"] == certificateId:
                # Update data
                certificate["data"].update(changes)
                certificate["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                certificates[i] = certificate
                
                # PRIMARY: Save to JSON
                self._save_user_certificates(userId, certificates)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_certificate_storage.update_certificate(userId, certificateId, changes)
                    except Exception as e:
                        print(f"⚠️ Supabase update failed (non-critical): {e}")
                
                return certificate
        
        return None


# Singleton instance
certificate_storage = CertificateStorage()


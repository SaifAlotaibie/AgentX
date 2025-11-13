"""
Work permit storage system using DUAL STORAGE: JSON files + Supabase.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from config.settings import LOG_PATH

# Create work_permits directory
WORK_PERMITS_PATH = LOG_PATH / "work_permits"
WORK_PERMITS_PATH.mkdir(parents=True, exist_ok=True)

# Import Supabase storage
try:
    from database.supabase_storage import supabase_work_permit_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available for work permits: {e}")
    SUPABASE_AVAILABLE = False


class WorkPermitStorage:
    """Manages work permit storage in JSON files + Supabase."""
    
    def __init__(self):
        """Initialize storage."""
        WORK_PERMITS_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_establishment_file(self, establishmentId: str) -> Path:
        """Get the JSON file path for an establishment's permits."""
        return WORK_PERMITS_PATH / f"{establishmentId}_permits.json"
    
    def _load_establishment_permits(self, establishmentId: str) -> List[Dict[str, Any]]:
        """Load all permits for an establishment."""
        file_path = self._get_establishment_file(establishmentId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_establishment_permits(self, establishmentId: str, permits: List[Dict[str, Any]]):
        """Save all permits for an establishment."""
        file_path = self._get_establishment_file(establishmentId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(permits, f, ensure_ascii=False, indent=2)
    
    def save_permit(self, establishmentId: str, permitId: str, permit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a work permit."""
        permits = self._load_establishment_permits(establishmentId)
        
        # Create permit object
        permit = {
            "permitId": permitId,
            "establishmentId": establishmentId,
            "data": permit_data,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # PRIMARY: Save to JSON
        permits.append(permit)
        self._save_establishment_permits(establishmentId, permits)
        
        # SECONDARY: Save to Supabase
        if SUPABASE_AVAILABLE:
            try:
                supabase_work_permit_storage.save_permit(establishmentId, permitId, permit_data)
            except Exception as e:
                print(f"⚠️ Supabase save failed (non-critical): {e}")
        
        return permit
    
    def get_permit(self, establishmentId: str, permitId: str) -> Optional[Dict[str, Any]]:
        """Get a specific permit."""
        permits = self._load_establishment_permits(establishmentId)
        
        for permit in permits:
            if permit["permitId"] == permitId:
                return permit
        
        return None
    
    def get_all_permits(self, establishmentId: str) -> List[Dict[str, Any]]:
        """Get all permits for an establishment."""
        return self._load_establishment_permits(establishmentId)
    
    def check_expiring_permits(self, establishmentId: str, days_threshold: int = 30) -> List[Dict[str, Any]]:
        """Get permits expiring within threshold days."""
        permits = self._load_establishment_permits(establishmentId)
        expiring = []
        
        today = datetime.now().date()
        threshold_date = today + timedelta(days=days_threshold)
        
        for permit in permits:
            expiry_str = permit["data"].get("expiry_date")
            if expiry_str:
                try:
                    expiry_date = datetime.fromisoformat(expiry_str.replace('Z', '')).date()
                    if today <= expiry_date <= threshold_date:
                        expiring.append(permit)
                except:
                    pass
        
        return expiring
    
    def update_permit(self, establishmentId: str, permitId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a permit."""
        permits = self._load_establishment_permits(establishmentId)
        
        for i, permit in enumerate(permits):
            if permit["permitId"] == permitId:
                # Update data
                permit["data"].update(changes)
                permit["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                permits[i] = permit
                
                # PRIMARY: Save to JSON
                self._save_establishment_permits(establishmentId, permits)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_work_permit_storage.update_permit(establishmentId, permitId, changes)
                    except Exception as e:
                        print(f"⚠️ Supabase update failed (non-critical): {e}")
                
                return permit
        
        return None


# Singleton instance
work_permit_storage = WorkPermitStorage()


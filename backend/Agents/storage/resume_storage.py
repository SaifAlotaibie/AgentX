"""
Resume storage system using DUAL STORAGE: JSON files + Supabase.
- JSON files: Primary storage (dev/debug, won't break system)
- Supabase: Secondary storage (production analytics)
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config.settings import RESUMES_PATH, LOG_PATH

# Import Supabase storage
try:
    from database.supabase_storage import supabase_resume_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available: {e}")
    SUPABASE_AVAILABLE = False

class ResumeStorage:
    """Manages resume storage in JSON files."""
    
    def __init__(self):
        """Initialize storage."""
        RESUMES_PATH.mkdir(parents=True, exist_ok=True)
        # Create user context directory for persistent memory
        self.context_dir = LOG_PATH / "user_context"
        self.context_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's resumes."""
        return RESUMES_PATH / f"{userId}_resumes.json"
    
    def _get_user_context_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's context (last resume, etc.)."""
        return self.context_dir / f"{userId}_context.json"
    
    def _load_user_resumes(self, userId: str) -> List[Dict[str, Any]]:
        """Load all resumes for a user."""
        file_path = self._get_user_file(userId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_user_resumes(self, userId: str, resumes: List[Dict[str, Any]]):
        """Save all resumes for a user."""
        file_path = self._get_user_file(userId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(resumes, f, ensure_ascii=False, indent=2)
    
    def save_resume(self, userId: str, resumeId: str, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a resume to JSON (primary) and Supabase (secondary).
        
        Args:
            userId: User ID
            resumeId: Resume ID
            resume_data: Resume content
            
        Returns:
            Saved resume with metadata
        """
        resumes = self._load_user_resumes(userId)
        
        # Create resume object
        resume = {
            "resumeId": resumeId,
            "userId": userId,
            "data": resume_data,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # PRIMARY: Save to JSON (will never fail)
        resumes.append(resume)
        self._save_user_resumes(userId, resumes)
        
        # Track as last accessed resume for persistent context
        self.set_last_accessed_resume(userId, resumeId)
        
        # SECONDARY: Save to Supabase (won't break if fails)
        if SUPABASE_AVAILABLE:
            try:
                supabase_resume_storage.save_resume(userId, resumeId, resume_data)
            except Exception as e:
                print(f"⚠️ Supabase save failed (non-critical): {e}")
        
        return resume
    
    def get_resume(self, userId: str, resumeId: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific resume.
        
        Args:
            userId: User ID
            resumeId: Resume ID
            
        Returns:
            Resume if found, None otherwise
        """
        resumes = self._load_user_resumes(userId)
        
        for resume in resumes:
            if resume["resumeId"] == resumeId:
                return resume
        
        return None
    
    def get_all_resumes(self, userId: str) -> List[Dict[str, Any]]:
        """
        Get all resumes for a user.
        
        Args:
            userId: User ID
            
        Returns:
            List of resumes
        """
        return self._load_user_resumes(userId)
    
    def set_last_accessed_resume(self, userId: str, resumeId: str):
        """
        Store the last accessed resume ID for persistent context.
        This allows the agent to remember which resume the user was working with
        across different chat sessions.
        
        Args:
            userId: User ID
            resumeId: Resume ID to remember
        """
        context_file = self._get_user_context_file(userId)
        context = {
            "last_resume_id": resumeId,
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        try:
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, ensure_ascii=False, indent=2)
            print(f"✓ Saved last accessed resume for {userId}: {resumeId}")
        except Exception as e:
            print(f"⚠️ Error saving user context: {e}")
    
    def get_last_accessed_resume(self, userId: str) -> Optional[str]:
        """
        Get the last accessed resume ID for persistent context.
        This is used when starting a new session to automatically know
        which resume the user wants to work with.
        
        Args:
            userId: User ID
            
        Returns:
            Resume ID if found, None otherwise
        """
        context_file = self._get_user_context_file(userId)
        
        if not context_file.exists():
            return None
        
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                context = json.load(f)
                resume_id = context.get("last_resume_id")
                
                if resume_id:
                    print(f"✓ Loaded last accessed resume for {userId}: {resume_id}")
                    return resume_id
                
        except Exception as e:
            print(f"⚠️ Error loading user context: {e}")
        
        return None
    
    def update_resume(self, userId: str, resumeId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a resume in JSON (primary) and Supabase (secondary).
        
        Args:
            userId: User ID
            resumeId: Resume ID
            changes: Changes to apply
            
        Returns:
            Updated resume if found, None otherwise
        """
        resumes = self._load_user_resumes(userId)
        
        for i, resume in enumerate(resumes):
            if resume["resumeId"] == resumeId:
                # Update data
                resume["data"].update(changes)
                resume["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                resumes[i] = resume
                
                # PRIMARY: Save to JSON
                self._save_user_resumes(userId, resumes)
                
                # Track as last accessed resume for persistent context
                self.set_last_accessed_resume(userId, resumeId)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_resume_storage.update_resume(userId, resumeId, changes)
                    except Exception as e:
                        print(f"⚠️ Supabase update failed (non-critical): {e}")
                
                return resume
        
        return None
    
    def delete_resume(self, userId: str, resumeId: str) -> bool:
        """
        Delete a resume from JSON (primary) and Supabase (secondary).
        
        Args:
            userId: User ID
            resumeId: Resume ID
            
        Returns:
            True if deleted, False if not found
        """
        resumes = self._load_user_resumes(userId)
        original_count = len(resumes)
        
        resumes = [r for r in resumes if r["resumeId"] != resumeId]
        
        if len(resumes) < original_count:
            # PRIMARY: Delete from JSON
            self._save_user_resumes(userId, resumes)
            
            # SECONDARY: Delete from Supabase
            if SUPABASE_AVAILABLE:
                try:
                    supabase_resume_storage.delete_resume(userId, resumeId)
                except Exception as e:
                    print(f"⚠️ Supabase delete failed (non-critical): {e}")
            
            return True
        
        return False

# Singleton instance
resume_storage = ResumeStorage()


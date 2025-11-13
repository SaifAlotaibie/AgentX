"""
Reminder storage system using DUAL STORAGE: JSON files + Supabase.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config.settings import LOG_PATH

# Create reminders directory
REMINDERS_PATH = LOG_PATH / "reminders"
REMINDERS_PATH.mkdir(parents=True, exist_ok=True)

# Import Supabase storage
try:
    from database.supabase_storage import supabase_reminder_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available for reminders: {e}")
    SUPABASE_AVAILABLE = False


class ReminderStorage:
    """Manages reminder storage in JSON files + Supabase."""
    
    def __init__(self):
        """Initialize storage."""
        REMINDERS_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's reminders."""
        return REMINDERS_PATH / f"{userId}_reminders.json"
    
    def _load_user_reminders(self, userId: str) -> List[Dict[str, Any]]:
        """Load all reminders for a user."""
        file_path = self._get_user_file(userId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_user_reminders(self, userId: str, reminders: List[Dict[str, Any]]):
        """Save all reminders for a user."""
        file_path = self._get_user_file(userId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
    
    def save_reminder(self, userId: str, reminderId: str, reminder_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a reminder."""
        reminders = self._load_user_reminders(userId)
        
        # Create reminder object
        reminder = {
            "reminderId": reminderId,
            "userId": userId,
            "data": reminder_data,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # PRIMARY: Save to JSON
        reminders.append(reminder)
        self._save_user_reminders(userId, reminders)
        
        # SECONDARY: Save to Supabase
        if SUPABASE_AVAILABLE:
            try:
                supabase_reminder_storage.save_reminder(userId, reminderId, reminder_data)
            except Exception as e:
                print(f"⚠️ Supabase save failed (non-critical): {e}")
        
        return reminder
    
    def get_pending_reminders(self, userId: str) -> List[Dict[str, Any]]:
        """Get all pending reminders for a user."""
        reminders = self._load_user_reminders(userId)
        
        pending = []
        for reminder in reminders:
            status = reminder.get("data", {}).get("status", "pending")
            if status == "pending":
                pending.append(reminder)
        
        return pending
    
    def mark_as_sent(self, userId: str, reminderId: str) -> bool:
        """Mark a reminder as sent."""
        return self.update_reminder(userId, reminderId, {"status": "sent"}) is not None
    
    def mark_as_actioned(self, userId: str, reminderId: str, action: Dict[str, Any]) -> bool:
        """Mark a reminder as actioned with action details."""
        return self.update_reminder(userId, reminderId, {
            "status": "actioned",
            "action_taken": action
        }) is not None
    
    def mark_as_dismissed(self, userId: str, reminderId: str) -> bool:
        """Mark a reminder as dismissed."""
        return self.update_reminder(userId, reminderId, {"status": "dismissed"}) is not None
    
    def update_reminder(self, userId: str, reminderId: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a reminder."""
        reminders = self._load_user_reminders(userId)
        
        for i, reminder in enumerate(reminders):
            if reminder["reminderId"] == reminderId:
                # Update data
                reminder["data"].update(changes)
                reminder["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                reminders[i] = reminder
                
                # PRIMARY: Save to JSON
                self._save_user_reminders(userId, reminders)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_reminder_storage.update_reminder(userId, reminderId, changes)
                    except Exception as e:
                        print(f"⚠️ Supabase update failed (non-critical): {e}")
                
                return reminder
        
        return None


# Singleton instance
reminder_storage = ReminderStorage()


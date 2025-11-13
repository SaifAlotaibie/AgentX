"""
Ticket storage system using DUAL STORAGE: JSON files + Supabase.
- JSON files: Primary storage (dev/debug, won't break system)
- Supabase: Secondary storage (production analytics)
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config.settings import LOG_PATH

TICKETS_PATH = LOG_PATH / "tickets"
TICKETS_PATH.mkdir(parents=True, exist_ok=True)

# Import Supabase storage
try:
    from database.supabase_storage import supabase_ticket_storage
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Supabase not available: {e}")
    SUPABASE_AVAILABLE = False

class TicketStorage:
    """Manages ticket storage in JSON files."""
    
    def __init__(self):
        """Initialize storage."""
        TICKETS_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file(self, userId: str) -> Path:
        """Get the JSON file path for a user's tickets."""
        return TICKETS_PATH / f"{userId}_tickets.json"
    
    def _load_user_tickets(self, userId: str) -> List[Dict[str, Any]]:
        """Load all tickets for a user."""
        file_path = self._get_user_file(userId)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_user_tickets(self, userId: str, tickets: List[Dict[str, Any]]):
        """Save all tickets for a user."""
        file_path = self._get_user_file(userId)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, ensure_ascii=False, indent=2)
    
    def save_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a ticket to JSON (primary) and Supabase (secondary).
        
        Args:
            ticket: Ticket data including userId
            
        Returns:
            Saved ticket
        """
        userId = ticket.get("userId")
        if not userId:
            raise ValueError("userId is required")
        
        # PRIMARY: Save to JSON
        tickets = self._load_user_tickets(userId)
        tickets.append(ticket)
        self._save_user_tickets(userId, tickets)
        
        # SECONDARY: Save to Supabase
        if SUPABASE_AVAILABLE:
            try:
                supabase_ticket_storage.save_ticket(ticket)
            except Exception as e:
                print(f"⚠️ Supabase save ticket failed (non-critical): {e}")
        
        return ticket
    
    def get_ticket(self, userId: str, ticketId: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific ticket.
        
        Args:
            userId: User ID
            ticketId: Ticket ID
            
        Returns:
            Ticket if found, None otherwise
        """
        tickets = self._load_user_tickets(userId)
        
        for ticket in tickets:
            if ticket["ticketId"] == ticketId:
                return ticket
        
        return None
    
    def get_all_tickets(self, userId: str) -> List[Dict[str, Any]]:
        """
        Get all tickets for a user.
        
        Args:
            userId: User ID
            
        Returns:
            List of tickets
        """
        return self._load_user_tickets(userId)
    
    def update_ticket(self, userId: str, ticketId: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a ticket in JSON (primary) and Supabase (secondary).
        
        Args:
            userId: User ID
            ticketId: Ticket ID
            updates: Updates to apply
            
        Returns:
            Updated ticket if found, None otherwise
        """
        tickets = self._load_user_tickets(userId)
        
        for i, ticket in enumerate(tickets):
            if ticket["ticketId"] == ticketId:
                ticket.update(updates)
                ticket["updatedAt"] = datetime.utcnow().isoformat() + "Z"
                tickets[i] = ticket
                
                # PRIMARY: Save to JSON
                self._save_user_tickets(userId, tickets)
                
                # SECONDARY: Update in Supabase
                if SUPABASE_AVAILABLE:
                    try:
                        supabase_ticket_storage.update_ticket(userId, ticketId, updates)
                    except Exception as e:
                        print(f"⚠️ Supabase update ticket failed (non-critical): {e}")
                
                return ticket
        
        return None

# Singleton instance
ticket_storage = TicketStorage()


"""
Ticket management tool for opening and closing support tickets.
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from utils.logger import log_action, log_error
from storage.ticket_storage import ticket_storage

class TicketTool:
    """Tool for managing support tickets."""
    
    def __init__(self):
        """Initialize the TicketTool."""
        pass
    
    def open_ticket(
        self,
        userId: str,
        ticket_type: str,
        description: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Open a new support ticket.
        
        Args:
            userId: User identifier
            ticket_type: Type of ticket (e.g., 'resume_update', 'resume_add', 'resume_delete')
            description: Description of the ticket
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with ticket details
        """
        try:
            # Generate unique ticket ID
            ticket_id = f"T{str(uuid.uuid4())[:8].upper()}"
            
            # Create timestamp
            created_at = datetime.utcnow().isoformat() + "Z"
            
            # Create ticket object
            ticket = {
                "ticketId": ticket_id,
                "userId": userId,
                "type": ticket_type,
                "description": description,
                "status": "open",
                "createdAt": created_at,
                "updatedAt": created_at
            }
            
            # Save to storage
            ticket_storage.save_ticket(ticket)
            
            result = ticket
            
            # Log the action
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="TicketTool.open_ticket",
                inputs={
                    "userId": userId,
                    "ticket_type": ticket_type,
                    "description": description
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="TicketTool.open_ticket",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    def close_ticket(
        self,
        ticketId: str,
        userId: str,
        sessionId: str = "system"
    ) -> Dict[str, Any]:
        """
        Close an existing support ticket.
        
        Args:
            ticketId: Ticket identifier
            userId: User identifier
            sessionId: Session identifier for logging
            
        Returns:
            Dictionary with updated ticket details
        """
        try:
            # Create timestamp
            closed_at = datetime.utcnow().isoformat() + "Z"
            
            # Update ticket in storage
            updated_ticket = ticket_storage.update_ticket(
                userId,
                ticketId,
                {"status": "closed", "closedAt": closed_at}
            )
            
            if updated_ticket:
                result = {
                    "ticketId": ticketId,
                    "userId": userId,
                    "status": "closed",
                    "closedAt": closed_at
                }
            else:
                result = {
                    "ticketId": ticketId,
                    "userId": userId,
                    "status": "error",
                    "message": "Ticket not found"
                }
            
            # Log the action
            log_action(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="TicketTool.close_ticket",
                inputs={
                    "ticketId": ticketId,
                    "userId": userId
                },
                outputs=result
            )
            
            return result
            
        except Exception as e:
            log_error(
                sessionId=sessionId,
                userId=userId,
                userRole="employee",
                tool="TicketTool.close_ticket",
                error=str(e),
                error_type=type(e).__name__
            )
            raise


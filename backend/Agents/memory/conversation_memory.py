"""
Conversation memory management for maintaining session context.
Persists conversation history to disk for continuity across sessions.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import SESSIONS_PATH

def get_user_memory(sessionId: str, userId: str) -> List[Dict[str, str]]:
    """
    Load conversation memory for a session.
    
    Args:
        sessionId: Session identifier
        userId: User identifier
        
    Returns:
        List of message dictionaries with 'role' and 'content' keys
    """
    session_file = SESSIONS_PATH / f"{sessionId}.json"
    
    # Create sessions directory if it doesn't exist
    SESSIONS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Load existing session or return empty list
    if session_file.exists():
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
        except Exception as e:
            print(f"Warning: Could not load session {sessionId}: {e}")
            return []
    
    return []

def save_memory(sessionId: str, messages: List[Dict[str, str]]) -> None:
    """
    Save conversation memory to disk.
    
    Args:
        sessionId: Session identifier
        messages: List of message dictionaries
    """
    session_file = SESSIONS_PATH / f"{sessionId}.json"
    
    # Create sessions directory if it doesn't exist
    SESSIONS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Save session data
    try:
        data = {
            "sessionId": sessionId,
            "messages": messages
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save session {sessionId}: {e}")

def add_message(sessionId: str, role: str, content: str) -> None:
    """
    Add a message to the conversation memory.
    
    Args:
        sessionId: Session identifier
        role: Message role ('user', 'assistant', 'system')
        content: Message content
    """
    # Load existing messages
    messages = get_user_memory(sessionId, "")
    
    # Append new message
    messages.append({
        "role": role,
        "content": content
    })
    
    # Save updated messages
    save_memory(sessionId, messages)

def clear_memory(sessionId: str) -> None:
    """
    Clear conversation memory for a session.
    
    Args:
        sessionId: Session identifier
    """
    session_file = SESSIONS_PATH / f"{sessionId}.json"
    
    if session_file.exists():
        try:
            session_file.unlink()
        except Exception as e:
            print(f"Warning: Could not clear session {sessionId}: {e}")

def get_session_metadata(sessionId: str) -> Optional[Dict[str, Any]]:
    """
    Get metadata about a session.
    
    Args:
        sessionId: Session identifier
        
    Returns:
        Dictionary with session metadata or None
    """
    session_file = SESSIONS_PATH / f"{sessionId}.json"
    
    if session_file.exists():
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            return {
                "sessionId": sessionId,
                "message_count": len(data.get('messages', [])),
                "file_size": session_file.stat().st_size,
                "last_modified": session_file.stat().st_mtime
            }
        except Exception as e:
            print(f"Warning: Could not get metadata for session {sessionId}: {e}")
            return None
    
    return None


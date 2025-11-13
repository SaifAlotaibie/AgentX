"""
Structured logging system for the Qiwa Agent.
Logs all interactions, actions, errors, and LLM calls to JSONL files.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import LOG_PATH

# TODO: In production, implement PII hashing/redaction for sensitive fields

def _get_timestamp() -> str:
    """Get current timestamp in ISO 8601 UTC format."""
    return datetime.utcnow().isoformat() + "Z"

def _write_log(filename: str, data: Dict[str, Any]) -> None:
    """
    Write a log entry to a JSONL file.
    
    Args:
        filename: Name of the log file (e.g., 'chat_logs.jsonl')
        data: Dictionary to log as JSON
    """
    log_file = LOG_PATH / filename
    
    # Ensure log directory exists
    LOG_PATH.mkdir(exist_ok=True)
    
    # Append log entry as newline-delimited JSON
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

def log_chat(
    sessionId: str,
    userId: str,
    userRole: str,
    role: str,
    message: str
) -> None:
    """
    Log a chat message.
    
    Args:
        sessionId: Session identifier
        userId: User identifier
        userRole: User role (employee, business_owner, service_provider)
        role: Message role (user, assistant, system)
        message: Message content
    """
    log_data = {
        "timestamp": _get_timestamp(),
        "sessionId": sessionId,
        "userId": userId,
        "userRole": userRole,
        "role": role,
        "message": message
    }
    _write_log("chat_logs.jsonl", log_data)

def log_action(
    sessionId: str,
    userId: str,
    userRole: str,
    tool: str,
    inputs: Dict[str, Any],
    outputs: Dict[str, Any]
) -> None:
    """
    Log a tool/action execution.
    
    Args:
        sessionId: Session identifier
        userId: User identifier
        userRole: User role
        tool: Tool name (e.g., 'ResumeTool.add_resume')
        inputs: Input parameters to the tool
        outputs: Output/result from the tool
    """
    log_data = {
        "timestamp": _get_timestamp(),
        "sessionId": sessionId,
        "userId": userId,
        "userRole": userRole,
        "tool": tool,
        "inputs": inputs,
        "outputs": outputs
    }
    _write_log("actions.jsonl", log_data)

def log_error(
    sessionId: str,
    userId: str,
    userRole: str,
    tool: str,
    error: str,
    error_type: Optional[str] = None
) -> None:
    """
    Log an error.
    
    Args:
        sessionId: Session identifier
        userId: User identifier
        userRole: User role
        tool: Tool or component where error occurred
        error: Error message
        error_type: Type of error (optional)
    """
    log_data = {
        "timestamp": _get_timestamp(),
        "sessionId": sessionId,
        "userId": userId,
        "userRole": userRole,
        "tool": tool,
        "error": error,
        "error_type": error_type
    }
    _write_log("errors.jsonl", log_data)

def log_llm(
    sessionId: str,
    model: str,
    prompt: str,
    response: str,
    tokens: Optional[int] = None,
    latency_ms: Optional[float] = None
) -> None:
    """
    Log an LLM call.
    
    Args:
        sessionId: Session identifier
        model: Model name (e.g., 'gpt-4o-mini')
        prompt: Input prompt to the model
        response: Response from the model
        tokens: Total tokens used (optional)
        latency_ms: Latency in milliseconds (optional)
    """
    log_data = {
        "timestamp": _get_timestamp(),
        "sessionId": sessionId,
        "model": model,
        "prompt": prompt,
        "response": response,
        "tokens": tokens,
        "latency_ms": latency_ms
    }
    _write_log("llm.jsonl", log_data)


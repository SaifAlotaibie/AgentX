"""
LLM wrapper with logging and support for multiple providers.
Supports both OpenAI and Ollama (local models).
"""

import time
from typing import Optional
from langchain.schema import HumanMessage, SystemMessage
from config.settings import OPENAI_API_KEY, MODEL_NAME, MODEL_TEMPERATURE, USE_LOCAL_LLM
from utils.logger import log_llm, log_error

# Initialize LLM cache
_llm_cache = {}

def get_llm(model_name: str = MODEL_NAME, temperature: float = MODEL_TEMPERATURE):
    """
    Get or create an LLM instance.
    
    Args:
        model_name: Name of the model to use
        temperature: Temperature parameter for generation
        
    Returns:
        LLM instance
    """
    cache_key = f"{model_name}_{temperature}"
    
    if cache_key not in _llm_cache:
        if USE_LOCAL_LLM:
            # Use Ollama for local model
            from langchain_ollama import ChatOllama
            
            # Model name from user: dengcao/Qwen3-Embedding-4B:Q5_K_M
            _llm_cache[cache_key] = ChatOllama(
                model="dengcao/Qwen3-Embedding-4B:Q5_K_M",
                temperature=temperature,
                base_url="http://localhost:11434"  # Default Ollama port
            )
        else:
            from langchain_openai import ChatOpenAI
            _llm_cache[cache_key] = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                openai_api_key=OPENAI_API_KEY
            )
    
    return _llm_cache[cache_key]

def call_llm(
    system_prompt: str,
    user_prompt: str,
    sessionId: str,
    model_name: str = MODEL_NAME,
    temperature: float = MODEL_TEMPERATURE
) -> str:
    """
    Call the LLM with system and user prompts, with logging.
    
    Args:
        system_prompt: System prompt to set context
        user_prompt: User prompt/question
        sessionId: Session identifier for logging
        model_name: Model to use
        temperature: Temperature parameter
        
    Returns:
        LLM response text
    """
    start_time = time.time()
    
    try:
        llm = get_llm(model_name, temperature)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Extract token usage if available
        tokens = None
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
            tokens = usage.get('total_tokens')
        
        # Log the LLM call
        log_llm(
            sessionId=sessionId,
            model=model_name if not USE_LOCAL_LLM else "dengcao/Qwen3-Embedding-4B:Q5_K_M",
            prompt=f"System: {system_prompt}\nUser: {user_prompt}",
            response=response_text,
            tokens=tokens,
            latency_ms=latency_ms
        )
        
        return response_text
        
    except Exception as e:
        log_error(
            sessionId=sessionId,
            userId="system",
            userRole="system",
            tool="llm_wrapper.call_llm",
            error=str(e),
            error_type=type(e).__name__
        )
        raise

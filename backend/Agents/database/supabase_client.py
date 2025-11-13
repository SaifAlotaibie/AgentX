"""
Supabase client initialization and utilities.
Single source of truth for Supabase connection.
"""

from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global Supabase client instance
_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance (singleton pattern).
    
    Returns:
        Supabase client instance
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("✓ Supabase client initialized")
        except Exception as e:
            logger.error(f"✗ Failed to initialize Supabase client: {e}")
            raise
    
    return _supabase_client

# Export client for direct import
supabase = get_supabase_client()

def test_connection() -> bool:
    """
    Test Supabase connection by querying schema_version table.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = get_supabase_client()
        
        # Try to query schema_version table
        response = client.table('schema_version').select('*').limit(1).execute()
        
        logger.info(f"✓ Supabase connection successful - Schema version: {response.data}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Supabase connection failed: {e}")
        return False

def safe_supabase_call(func):
    """
    Decorator for safe Supabase calls with error handling.
    Won't crash the system if Supabase fails.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Supabase operation failed: {func.__name__} - {e}")
            return None
    return wrapper


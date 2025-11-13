"""Database package for Supabase integration."""
from .supabase_client import supabase, test_connection

__all__ = ['supabase', 'test_connection']


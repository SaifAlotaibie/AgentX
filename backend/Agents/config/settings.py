"""
Configuration settings for the Qiwa Agent System.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent.parent / "data"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Backend API Configuration
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3000/api")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))

# Language Configuration - ARABIC ONLY
DEFAULT_LANGUAGE = "ar"
FORCE_ARABIC = True  # Force all responses in Arabic

# Logging Configuration
LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")
LOG_PATH = BASE_DIR / LOG_DIRECTORY
SESSIONS_PATH = LOG_PATH / "sessions"

# Feature Flags
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"

# Development Mode - Enable ALL features for testing (bypasses user_type restrictions)
DEV_MODE_ALL_FEATURES = True  # Set to False in production!

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://womyztswwrnyazqglryg.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvbXl6dHN3d3JueWF6cWdscnlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NTAzMDgsImV4cCI6MjA3ODUyNjMwOH0.C-DRpZva7Xc5agXOmXb1sIQzlv89tXyH_gebcmLll1Q")

# Mock/Dev User for testing without authentication
MOCK_USER_ID = "a1b2c3d4-5678-90ab-cdef-123456789000"  # Fake but valid UUID
MOCK_USER_NAME = "زياد الحربي"
MOCK_USER_PHONE = "+966501234567"
MOCK_USER_EMAIL = "ziyad.dev@qiwa.test"
MOCK_USER_TYPE = "employee"  # Can be: employee, business_owner, service_provider
MOCK_USER_ESTABLISHMENT_ID = "EST12345"  # For testing business owner features

# Feature Configuration
PROACTIVE_REMINDERS_ENABLED = True  # Enable proactive reminder system

# FAQ Data Files
FAQ_RAG_FILE = DATA_DIR / "hrsd_faqs_rag.json"
SERVICES_FILE = DATA_DIR / "services_converted.json"

# Ensure log directories exist
LOG_PATH.mkdir(exist_ok=True)
SESSIONS_PATH.mkdir(exist_ok=True)

# Resume storage (in-memory for MVP - will move to DB later)
RESUMES_PATH = LOG_PATH / "resumes"
RESUMES_PATH.mkdir(exist_ok=True)

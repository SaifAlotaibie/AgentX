#!/usr/bin/env python3
"""
Verification script to ensure the Qiwa Agent System is properly set up.
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} MISSING: {path}")
        return False

def check_directory(path, description):
    """Check if a directory exists."""
    if Path(path).is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} MISSING: {path}")
        return False

def verify_setup():
    """Verify the complete setup."""
    print("=" * 60)
    print("Qiwa Agent System - Setup Verification")
    print("=" * 60)
    
    all_checks = []
    
    print("\n📦 Core Files:")
    all_checks.append(check_file("app.py", "FastAPI Server"))
    all_checks.append(check_file("requirements.txt", "Dependencies"))
    all_checks.append(check_file("README.md", "Documentation"))
    all_checks.append(check_file("QUICKSTART.md", "Quick Start Guide"))
    all_checks.append(check_file("sample_client.html", "Sample Client"))
    all_checks.append(check_file("test_agent.py", "Test Suite"))
    
    print("\n⚙️  Configuration:")
    all_checks.append(check_file(".env.example", "Env Template"))
    all_checks.append(check_file("config/settings.py", "Settings"))
    
    print("\n🔧 Utilities:")
    all_checks.append(check_file("utils/logger.py", "Logger"))
    all_checks.append(check_file("utils/llm_wrapper.py", "LLM Wrapper"))
    all_checks.append(check_file("utils/language_detector.py", "Language Detector"))
    
    print("\n🛠️  Tools:")
    all_checks.append(check_file("tools/shared/ticket_tool.py", "Ticket Tool"))
    all_checks.append(check_file("tools/employee/resume_tool.py", "Resume Tool"))
    all_checks.append(check_file("tools/shared/knowledge_tool.py", "Knowledge Tool"))
    
    print("\n🤖 Agent System:")
    all_checks.append(check_file("agents/base_agent.py", "Base Agent"))
    all_checks.append(check_file("agents/employee_agent.py", "Employee Agent"))
    
    print("\n🔀 Routing:")
    all_checks.append(check_file("routers/employee_router.py", "Employee Router"))
    
    print("\n💾 Memory:")
    all_checks.append(check_file("memory/conversation_memory.py", "Conversation Memory"))
    
    print("\n📁 Directories:")
    all_checks.append(check_directory("logs", "Logs Directory"))
    all_checks.append(check_directory("logs/sessions", "Sessions Directory"))
    
    print("\n📊 Data Files (External):")
    data_dir = Path("../../data")
    all_checks.append(check_file(data_dir / "hrsd_faqs_rag.json", "FAQ Data"))
    all_checks.append(check_file(data_dir / "services_converted.json", "Services Data"))
    
    print("\n" + "=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print(f"✓ ALL CHECKS PASSED ({passed}/{total})")
        print("=" * 60)
        print("\n✨ Setup is complete and ready!")
        print("\n📚 Next Steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run tests: python3 test_agent.py")
        print("  3. Start server: uvicorn app:app --reload")
        print("  4. Open sample_client.html in browser")
        return True
    else:
        print(f"✗ SOME CHECKS FAILED ({passed}/{total})")
        print("=" * 60)
        print("\n⚠️  Please review missing files above")
        return False

if __name__ == "__main__":
    success = verify_setup()
    sys.exit(0 if success else 1)


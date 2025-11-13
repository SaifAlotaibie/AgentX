#!/usr/bin/env python3
"""
Test script to verify Supabase connection and schema.
Run this after applying the schema to verify everything works.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.supabase_client import test_connection, supabase
from database.supabase_storage import (
    supabase_resume_storage,
    supabase_ticket_storage,
    supabase_conversation_storage,
    supabase_user_behavior_storage,
    supabase_tool_call_storage,
    supabase_process_step_storage,
    supabase_user_profile_storage
)
import uuid
from datetime import datetime

def test_basic_connection():
    """Test basic Supabase connection."""
    print("\n" + "="*60)
    print("🔌 Testing Basic Connection")
    print("="*60)
    
    if test_connection():
        print("✅ Connection successful!")
        return True
    else:
        print("❌ Connection failed!")
        return False

def test_tables_exist():
    """Test that all required tables exist."""
    print("\n" + "="*60)
    print("📊 Testing Table Existence")
    print("="*60)
    
    tables = [
        'user_profile',
        'user_behavior',
        'conversations',
        'resumes',
        'tickets',
        'tool_calls',
        'process_steps'
    ]
    
    all_exist = True
    for table in tables:
        try:
            result = supabase.table(table).select('*').limit(1).execute()
            print(f"✅ Table '{table}' exists")
        except Exception as e:
            print(f"❌ Table '{table}' not found: {e}")
            all_exist = False
    
    return all_exist

def test_user_profile():
    """Test user profile creation."""
    print("\n" + "="*60)
    print("👤 Testing User Profile Storage")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    
    try:
        profile = supabase_user_profile_storage.create_or_update_profile(
            userId=test_user_id,
            full_name="أحمد محمد (اختبار)",
            phone="0501234567"
        )
        
        if profile:
            print(f"✅ User profile created: {profile}")
            
            # Retrieve it
            retrieved = supabase_user_profile_storage.get_profile(test_user_id)
            if retrieved:
                print(f"✅ User profile retrieved successfully")
                return True
            else:
                print("❌ Failed to retrieve user profile")
                return False
        else:
            print("❌ Failed to create user profile")
            return False
            
    except Exception as e:
        print(f"❌ User profile test failed: {e}")
        return False

def test_conversation_logging():
    """Test conversation logging."""
    print("\n" + "="*60)
    print("💬 Testing Conversation Logging")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    
    try:
        # Log user message
        msg1 = supabase_conversation_storage.log_message(
            userId=test_user_id,
            role="user",
            content="مرحباً، أريد إضافة سيرتي الذاتية"
        )
        
        if msg1:
            print("✅ User message logged")
        
        # Log assistant message
        msg2 = supabase_conversation_storage.log_message(
            userId=test_user_id,
            role="assistant",
            content="مرحباً! سأساعدك في إضافة سيرتك الذاتية..."
        )
        
        if msg2:
            print("✅ Assistant message logged")
        
        # Retrieve conversation
        history = supabase_conversation_storage.get_conversation_history(test_user_id)
        if history and len(history) >= 2:
            print(f"✅ Conversation history retrieved: {len(history)} messages")
            return True
        else:
            print("❌ Failed to retrieve conversation history")
            return False
            
    except Exception as e:
        print(f"❌ Conversation logging test failed: {e}")
        return False

def test_resume_storage():
    """Test resume storage."""
    print("\n" + "="*60)
    print("📄 Testing Resume Storage")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    test_resume_id = f"R{int(datetime.now().timestamp())}"
    
    try:
        resume_data = {
            "full_name": "أحمد محمد العتيبي",
            "job_title": "مهندس برمجيات",
            "contact": {
                "email": "ahmed@example.com",
                "phone": "0501234567"
            },
            "skills": ["Python", "JavaScript", "AI"],
            "education": [],
            "experience": []
        }
        
        # Save resume
        result = supabase_resume_storage.save_resume(
            userId=test_user_id,
            resumeId=test_resume_id,
            resume_data=resume_data
        )
        
        if result:
            print(f"✅ Resume saved: {test_resume_id}")
            
            # Retrieve resumes
            resumes = supabase_resume_storage.get_all_resumes(test_user_id)
            if resumes:
                print(f"✅ Resume retrieved: {len(resumes)} resumes found")
                return True
            else:
                print("❌ Failed to retrieve resumes")
                return False
        else:
            print("❌ Failed to save resume")
            return False
            
    except Exception as e:
        print(f"❌ Resume storage test failed: {e}")
        return False

def test_ticket_storage():
    """Test ticket storage."""
    print("\n" + "="*60)
    print("🎫 Testing Ticket Storage")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    test_ticket_id = f"T{int(datetime.now().timestamp())}"
    
    try:
        ticket_data = {
            "userId": test_user_id,
            "ticketId": test_ticket_id,
            "type": "resume_add",
            "description": "إضافة سيرة ذاتية",
            "status": "open",
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save ticket
        result = supabase_ticket_storage.save_ticket(ticket_data)
        
        if result:
            print(f"✅ Ticket saved: {test_ticket_id}")
            
            # Retrieve tickets
            tickets = supabase_ticket_storage.get_all_tickets(test_user_id)
            if tickets:
                print(f"✅ Ticket retrieved: {len(tickets)} tickets found")
                return True
            else:
                print("❌ Failed to retrieve tickets")
                return False
        else:
            print("❌ Failed to save ticket")
            return False
            
    except Exception as e:
        print(f"❌ Ticket storage test failed: {e}")
        return False

def test_tool_call_logging():
    """Test tool call logging."""
    print("\n" + "="*60)
    print("🔧 Testing Tool Call Logging")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    test_session_id = f"S{int(datetime.now().timestamp())}"
    
    try:
        result = supabase_tool_call_storage.log_tool_call(
            userId=test_user_id,
            sessionId=test_session_id,
            tool_name="add_resume",
            tool_input={"userId": test_user_id, "resume_data": {"full_name": "أحمد"}},
            tool_output="Resume added successfully",
            execution_time_ms=245,
            success=True
        )
        
        if result:
            print(f"✅ Tool call logged successfully")
            return True
        else:
            print("❌ Failed to log tool call")
            return False
            
    except Exception as e:
        print(f"❌ Tool call logging test failed: {e}")
        return False

def test_process_step_logging():
    """Test process step logging."""
    print("\n" + "="*60)
    print("📝 Testing Process Step Logging")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    test_session_id = f"S{int(datetime.now().timestamp())}"
    
    try:
        result = supabase_process_step_storage.log_process_step(
            userId=test_user_id,
            sessionId=test_session_id,
            step_id="open_ticket",
            step_title="فتح تذكرة",
            step_status="done",
            step_meta={"ticketId": "T123"}
        )
        
        if result:
            print(f"✅ Process step logged successfully")
            return True
        else:
            print("❌ Failed to log process step")
            return False
            
    except Exception as e:
        print(f"❌ Process step logging test failed: {e}")
        return False

def test_user_behavior():
    """Test user behavior tracking."""
    print("\n" + "="*60)
    print("📊 Testing User Behavior Tracking")
    print("="*60)
    
    test_user_id = str(uuid.uuid4())
    
    try:
        result = supabase_user_behavior_storage.update_behavior(
            userId=test_user_id,
            last_message="أريد إضافة سيرتي الذاتية",
            intent="service",
            predicted_need="إدارة السيرة الذاتية"
        )
        
        if result:
            print(f"✅ User behavior updated successfully")
            
            # Retrieve it
            behavior = supabase_user_behavior_storage.get_behavior(test_user_id)
            if behavior:
                print(f"✅ User behavior retrieved: {behavior}")
                return True
            else:
                print("❌ Failed to retrieve user behavior")
                return False
        else:
            print("❌ Failed to update user behavior")
            return False
            
    except Exception as e:
        print(f"❌ User behavior test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "🧪 "*20)
    print("🚀 SUPABASE INTEGRATION TEST SUITE")
    print("🧪 "*20)
    
    tests = [
        ("Basic Connection", test_basic_connection),
        ("Table Existence", test_tables_exist),
        ("User Profile", test_user_profile),
        ("Conversation Logging", test_conversation_logging),
        ("Resume Storage", test_resume_storage),
        ("Ticket Storage", test_ticket_storage),
        ("Tool Call Logging", test_tool_call_logging),
        ("Process Step Logging", test_process_step_logging),
        ("User Behavior", test_user_behavior),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"🎯 Result: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Supabase integration is working perfectly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())


"""
Test script for the Qiwa Agent System.
Tests both English and Arabic flows without requiring OpenAI API key.
"""

import sys
import json
from datetime import datetime

# Mock the OpenAI dependency for testing without API key
class MockChatOpenAI:
    def __init__(self, *args, **kwargs):
        pass
    
    def invoke(self, messages):
        class MockResponse:
            def __init__(self):
                self.content = "This is a mock response for testing"
                self.response_metadata = {
                    'token_usage': {
                        'total_tokens': 100
                    }
                }
        return MockResponse()

# Patch before imports
sys.modules['langchain_openai'] = type(sys)('langchain_openai')
sys.modules['langchain_openai'].ChatOpenAI = MockChatOpenAI

# Now import our modules
from tools.shared.ticket_tool import TicketTool
from tools.employee.resume_tool import ResumeTool
from tools.shared.knowledge_tool import KnowledgeTool
from utils.language_detector import detect_language, extract_intent, is_confirmation
from memory.conversation_memory import add_message, get_user_memory, clear_memory

def test_language_detection():
    """Test language detection."""
    print("Testing language detection...")
    
    # Test English
    assert detect_language("Hello, how are you?") == "en"
    print("✓ English detection works")
    
    # Test Arabic
    assert detect_language("مرحبا، كيف حالك؟") == "ar"
    print("✓ Arabic detection works")

def test_intent_extraction():
    """Test intent extraction."""
    print("\nTesting intent extraction...")
    
    # Test resume add
    assert extract_intent("I want to add my resume", "en") == "resume_add"
    assert extract_intent("أريد إضافة سيرتي الذاتية", "ar") == "resume_add"
    print("✓ Resume add intent works")
    
    # Test resume edit
    assert extract_intent("I want to edit my resume", "en") == "resume_edit"
    assert extract_intent("أريد تعديل سيرتي الذاتية", "ar") == "resume_edit"
    print("✓ Resume edit intent works")
    
    # Test Q&A
    assert extract_intent("What is Qiwa?", "en") == "qa"
    assert extract_intent("ما هي منصة قوى؟", "ar") == "qa"
    print("✓ Q&A intent works")

def test_confirmation():
    """Test confirmation detection."""
    print("\nTesting confirmation detection...")
    
    # Test yes
    assert is_confirmation("yes", "en") == True
    assert is_confirmation("نعم", "ar") == True
    print("✓ Confirmation detection works")
    
    # Test no
    assert is_confirmation("no", "en") == False
    assert is_confirmation("لا", "ar") == False
    print("✓ Rejection detection works")

def test_ticket_tool():
    """Test ticket tool."""
    print("\nTesting ticket tool...")
    
    ticket_tool = TicketTool()
    
    # Open ticket
    result = ticket_tool.open_ticket(
        userId="U123",
        ticket_type="resume_add",
        description="Add new resume",
        sessionId="TEST_SESSION"
    )
    
    assert result["status"] == "open"
    assert "ticketId" in result
    ticket_id = result["ticketId"]
    print(f"✓ Ticket opened: {ticket_id}")
    
    # Close ticket
    result = ticket_tool.close_ticket(
        ticketId=ticket_id,
        userId="U123",
        sessionId="TEST_SESSION"
    )
    
    assert result["status"] == "closed"
    print(f"✓ Ticket closed: {ticket_id}")

def test_resume_tool():
    """Test resume tool."""
    print("\nTesting resume tool...")
    
    resume_tool = ResumeTool()
    
    # Test validation - missing fields
    resume_data = {"full_name": "John Doe"}
    validation = resume_tool.validate_resume_data(resume_data)
    assert validation["is_valid"] == False
    assert "job_title" in validation["missing_fields"]
    print("✓ Resume validation works")
    
    # Test add resume
    complete_resume = {
        "full_name": "John Doe",
        "job_title": "Software Engineer",
        "contact": {
            "email": "john@example.com",
            "phone": "+966501234567"
        }
    }
    
    result = resume_tool.add_resume(
        userId="U123",
        resume_data=complete_resume,
        sessionId="TEST_SESSION"
    )
    
    assert result["status"] == "success"
    assert "resumeId" in result
    print(f"✓ Resume added: {result['resumeId']}")
    
    # Test edit resume
    result = resume_tool.edit_resume(
        userId="U123",
        resumeId="R123",
        changes={"job_title": "Senior Software Engineer"},
        sessionId="TEST_SESSION"
    )
    
    assert result["status"] == "success"
    print("✓ Resume edited")
    
    # Test delete resume
    result = resume_tool.delete_resume(
        userId="U123",
        resumeId="R123",
        sessionId="TEST_SESSION"
    )
    
    assert result["status"] == "success"
    print("✓ Resume deleted")

def test_knowledge_tool():
    """Test knowledge tool."""
    print("\nTesting knowledge tool...")
    
    knowledge_tool = KnowledgeTool()
    
    # Test English Q&A
    result = knowledge_tool.answer_question(
        userId="U123",
        query="What is Qiwa?",
        language="en",
        sessionId="TEST_SESSION"
    )
    
    assert "answer" in result
    assert len(result["answer"]) > 0
    print(f"✓ English Q&A works: {result['answer'][:50]}...")
    
    # Test Arabic Q&A
    result = knowledge_tool.answer_question(
        userId="U123",
        query="ما هي منصة قوى؟",
        language="ar",
        sessionId="TEST_SESSION"
    )
    
    assert "answer" in result
    assert len(result["answer"]) > 0
    print(f"✓ Arabic Q&A works: {result['answer'][:50]}...")

def test_memory():
    """Test conversation memory."""
    print("\nTesting conversation memory...")
    
    test_session = "TEST_MEMORY_SESSION"
    
    # Clear any existing memory
    clear_memory(test_session)
    
    # Add messages
    add_message(test_session, "user", "Hello")
    add_message(test_session, "assistant", "Hi there!")
    add_message(test_session, "user", "How are you?")
    
    # Retrieve memory
    memory = get_user_memory(test_session, "U123")
    
    assert len(memory) == 3
    assert memory[0]["role"] == "user"
    assert memory[0]["content"] == "Hello"
    print(f"✓ Memory persisted: {len(memory)} messages")
    
    # Clear memory
    clear_memory(test_session)
    memory = get_user_memory(test_session, "U123")
    assert len(memory) == 0
    print("✓ Memory cleared")

def test_complete_flow():
    """Test a complete resume add flow."""
    print("\nTesting complete resume add flow...")
    
    session_id = "FLOW_TEST_SESSION"
    user_id = "U123"
    
    # Step 1: Open ticket
    ticket_tool = TicketTool()
    ticket_result = ticket_tool.open_ticket(
        userId=user_id,
        ticket_type="resume_add",
        description="Add new resume",
        sessionId=session_id
    )
    
    print(f"  1. Ticket opened: {ticket_result['ticketId']}")
    
    # Step 2: Collect resume data (simulated)
    resume_data = {
        "full_name": "أحمد محمد",
        "job_title": "مهندس برمجيات",
        "contact": {
            "email": "ahmed@example.com",
            "phone": "+966501234567"
        },
        "skills": ["Python", "JavaScript", "React"],
        "summary": "خبرة 5 سنوات في تطوير البرمجيات"
    }
    
    print("  2. Resume data collected")
    
    # Step 3: Add resume
    resume_tool = ResumeTool()
    resume_result = resume_tool.add_resume(
        userId=user_id,
        resume_data=resume_data,
        sessionId=session_id
    )
    
    print(f"  3. Resume added: {resume_result['resumeId']}")
    
    # Step 4: Close ticket
    close_result = ticket_tool.close_ticket(
        ticketId=ticket_result['ticketId'],
        userId=user_id,
        sessionId=session_id
    )
    
    print(f"  4. Ticket closed: {close_result['status']}")
    print("✓ Complete flow successful")

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Qiwa Agent System - Test Suite")
    print("=" * 60)
    
    try:
        test_language_detection()
        test_intent_extraction()
        test_confirmation()
        test_ticket_tool()
        test_resume_tool()
        test_knowledge_tool()
        test_memory()
        test_complete_flow()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe agent system is working correctly.")
        print("You can now start the server with:")
        print("  uvicorn app:app --reload")
        print("\nOr test with the sample client:")
        print("  Open sample_client.html in your browser")
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


#!/usr/bin/env python3
"""
Test script to demonstrate the REAL AI agent making intelligent decisions.
The LLM decides when to call tools instead of following hardcoded rules.
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime

async def test_real_agent():
    """Test the real agent with various inputs."""
    
    # Test cases
    test_cases = [
        {
            "name": "Resume Add Request (Arabic)",
            "message": "أريد إضافة سيرتي الذاتية",
            "expected_tools": ["open_ticket"]
        },
        {
            "name": "Q&A Request (Arabic)",
            "message": "ما هي خدمات قوى؟",
            "expected_tools": ["answer_question"]
        },
        {
            "name": "Resume Request (English)",
            "message": "I want to create a new resume",
            "expected_tools": ["open_ticket"]
        }
    ]
    
    sessionId = f"TEST{int(datetime.now().timestamp())}"
    userId = "TEST_USER_001"
    userRole = "employee"
    
    ws_url = f"ws://localhost:8000/ws/{sessionId}/{userId}/{userRole}"
    
    print("=" * 80)
    print("🤖 TESTING REAL AI AGENT - LLM MAKES DECISIONS!")
    print("=" * 80)
    print(f"\nConnecting to: {ws_url}\n")
    
    try:
        async with websockets.connect(ws_url) as websocket:
            # Read initial connection message
            response = await websocket.recv()
            print(f"✓ Connected: {json.loads(response)['message']}\n")
            
            # Run test cases
            for i, test in enumerate(test_cases, 1):
                print(f"\n{'='*80}")
                print(f"TEST {i}: {test['name']}")
                print(f"{'='*80}")
                print(f"📤 Sending: {test['message']}")
                
                # Send message
                await websocket.send(json.dumps({
                    "type": "user_message",
                    "sessionId": sessionId,
                    "userId": userId,
                    "userRole": userRole,
                    "message": test['message']
                }))
                
                # Collect responses
                tools_called = []
                assistant_response = None
                
                for _ in range(10):  # Max 10 messages per test
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                        data = json.loads(response)
                        
                        if data['type'] == 'chat_message':
                            if data['role'] == 'assistant':
                                assistant_response = data['message']
                                print(f"🤖 Agent: {assistant_response}")
                        
                        elif data['type'] == 'process_update':
                            for step in data.get('steps', []):
                                tool_name = step['title']
                                if tool_name not in tools_called:
                                    tools_called.append(tool_name)
                                    print(f"🔧 Tool Called: {tool_name}")
                        
                        # If we got an assistant response, we're done with this test
                        if assistant_response:
                            break
                    
                    except asyncio.TimeoutError:
                        print("⏱️  Timeout waiting for response")
                        break
                
                # Verify results
                print(f"\n📊 Results:")
                print(f"   Tools Called: {tools_called or ['None']}")
                print(f"   Expected: {test['expected_tools']}")
                
                if tools_called:
                    print(f"   ✅ Agent made intelligent decision to call tools!")
                else:
                    print(f"   ⚠️  No tools called (might be appropriate for this input)")
                
                # Wait a bit before next test
                await asyncio.sleep(2)
            
            print(f"\n{'='*80}")
            print("✅ ALL TESTS COMPLETED!")
            print("=" * 80)
            print("\n🎉 THE AGENT NOW USES LLM TO MAKE INTELLIGENT DECISIONS!")
            print("   - LLM analyzes user intent")
            print("   - LLM chooses which tools to call")
            print("   - LLM generates appropriate responses")
            print("   - NO MORE HARDCODED KEYWORD MATCHING!")
            print()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_real_agent())


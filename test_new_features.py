"""
Quick test script to verify all new features are working.
Run after migrating Supabase and restarting backend.
"""

import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = "a1b2c3d4-5678-90ab-cdef-123456789000"  # Mock user
ESTABLISHMENT_ID = "EST12345"

def test_endpoint(name, url):
    """Test an endpoint and print results."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Count: {data.get('count', 0)}")
            print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests."""
    print("🧪 TESTING NEW AGENTX FEATURES")
    print("="*60)
    
    # Test health check
    test_endpoint("Health Check", f"{BASE_URL}/health")
    
    # Test existing endpoints
    test_endpoint("Resumes", f"{BASE_URL}/resumes/{USER_ID}")
    test_endpoint("Tickets", f"{BASE_URL}/tickets/{USER_ID}")
    
    # Test NEW endpoints
    test_endpoint("Contracts (NEW)", f"{BASE_URL}/contracts/{USER_ID}")
    test_endpoint("Certificates (NEW)", f"{BASE_URL}/certificates/{USER_ID}")
    test_endpoint("Work Permits (NEW)", f"{BASE_URL}/permits/{ESTABLISHMENT_ID}")
    test_endpoint("Reminders (NEW)", f"{BASE_URL}/reminders/{USER_ID}")
    
    print("\n" + "="*60)
    print("🎉 TEST COMPLETE!")
    print("\nNOTE: Empty results are normal if no data exists yet.")
    print("Try using the voice call to create some data!")
    print("="*60)

if __name__ == "__main__":
    main()


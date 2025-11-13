"""
Seed demo data for testing all new features.
Run this to populate contracts, certificates, work permits, and reminders.
"""

import uuid
from datetime import datetime, timedelta
from storage.contract_storage import contract_storage
from storage.certificate_storage import certificate_storage
from storage.work_permit_storage import work_permit_storage
from storage.reminder_storage import reminder_storage

# Mock user ID (matching what frontend uses in sessionStorage)
MOCK_USER_ID = "demo_user"  # Frontend uses this
MOCK_ESTABLISHMENT_ID = "EST12345"

def seed_contracts():
    """Add demo employment contracts."""
    print("\n📄 Adding demo contracts...")
    
    contracts = [
        {
            "contractId": f"CON{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employer_id": "EMP001",
                "employer_name": "شركة أرامكو السعودية",
                "job_title": "مهندس برمجيات أول",
                "salary": 15000.00,
                "start_date": "2022-01-01",
                "end_date": "2025-01-01",
                "status": "active",
                "renewal_history": []
            }
        },
        {
            "contractId": f"CON{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employer_id": "EMP002",
                "employer_name": "شركة الاتصالات السعودية (STC)",
                "job_title": "محلل بيانات",
                "salary": 12000.00,
                "start_date": "2023-03-15",
                "end_date": "2024-12-31",
                "status": "active",
                "renewal_history": [
                    {"date": "2024-01-01", "new_salary": 12000}
                ]
            }
        }
    ]
    
    for contract in contracts:
        contract_storage.save_contract(MOCK_USER_ID, contract["contractId"], contract["data"])
        print(f"✅ Added contract: {contract['contractId']} - {contract['data']['employer_name']}")
    
    print(f"✅ Total contracts added: {len(contracts)}")

def seed_certificates():
    """Add demo certificate requests."""
    print("\n📜 Adding demo certificates...")
    
    certificates = [
        {
            "certificateId": f"CERT{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "type": "salary",
                "purpose": "visa",
                "status": "ready",
                "request_date": (datetime.now() - timedelta(days=5)).isoformat() + "Z",
                "ready_date": (datetime.now() - timedelta(days=1)).isoformat() + "Z",
                "employee_data": {
                    "name": "زياد الحربي",
                    "position": "مهندس برمجيات",
                    "salary": 15000,
                    "employment_duration": "3 سنوات"
                }
            }
        },
        {
            "certificateId": f"CERT{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "type": "experience",
                "purpose": "new_job",
                "status": "processing",
                "request_date": (datetime.now() - timedelta(days=2)).isoformat() + "Z",
                "employee_data": {
                    "name": "زياد الحربي",
                    "position": "مهندس برمجيات",
                    "employment_duration": "3 سنوات"
                }
            }
        },
        {
            "certificateId": f"CERT{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "type": "salary",
                "purpose": "loan",
                "status": "requested",
                "request_date": datetime.now().isoformat() + "Z",
                "employee_data": {}
            }
        }
    ]
    
    for cert in certificates:
        certificate_storage.save_certificate(MOCK_USER_ID, cert["certificateId"], cert["data"])
        print(f"✅ Added certificate: {cert['certificateId']} - {cert['data']['type']} ({cert['data']['status']})")
    
    print(f"✅ Total certificates added: {len(certificates)}")

def seed_work_permits():
    """Add demo work permits."""
    print("\n🛡️ Adding demo work permits...")
    
    permits = [
        {
            "permitId": f"PER{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employee_id": "E001",
                "employee_name": "أحمد محمد",
                "nationality": "مصري",
                "job_title": "مهندس مدني",
                "issue_date": "2023-01-01",
                "expiry_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),  # Expires in 15 days
                "status": "expiring_soon"
            }
        },
        {
            "permitId": f"PER{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employee_id": "E002",
                "employee_name": "محمد علي",
                "nationality": "يمني",
                "job_title": "فني كهرباء",
                "issue_date": "2023-06-01",
                "expiry_date": (datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d"),
                "status": "active"
            }
        },
        {
            "permitId": f"PER{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employee_id": "E003",
                "employee_name": "فاطمة حسن",
                "nationality": "سوداني",
                "job_title": "محاسبة",
                "issue_date": "2023-03-15",
                "expiry_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),  # Expires in 5 days!
                "status": "expiring_soon"
            }
        },
        {
            "permitId": f"PER{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employee_id": "E004",
                "employee_name": "خالد إبراهيم",
                "nationality": "أردني",
                "job_title": "مدير مشروع",
                "issue_date": "2022-01-01",
                "expiry_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),  # Already expired!
                "status": "expired"
            }
        },
        {
            "permitId": f"PER{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "employee_id": "E005",
                "employee_name": "سارة أحمد",
                "nationality": "لبناني",
                "job_title": "مصممة جرافيك",
                "issue_date": "2023-09-01",
                "expiry_date": (datetime.now() + timedelta(days=200)).strftime("%Y-%m-%d"),
                "status": "active"
            }
        }
    ]
    
    for permit in permits:
        work_permit_storage.save_permit(MOCK_ESTABLISHMENT_ID, permit["permitId"], permit["data"])
        status_emoji = "⚠️" if permit["data"]["status"] in ["expiring_soon", "expired"] else "✅"
        print(f"{status_emoji} Added permit: {permit['permitId']} - {permit['data']['employee_name']} ({permit['data']['status']})")
    
    print(f"✅ Total permits added: {len(permits)}")

def seed_reminders():
    """Add demo proactive reminders."""
    print("\n🔔 Adding demo reminders...")
    
    reminders = [
        {
            "reminderId": f"REM{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "reminder_type": "contract_expiry",
                "related_entity_id": "CON123",
                "message": "⚠️ عقدك مع شركة أرامكو ينتهي خلال 30 يوم. هل تريد طلب التجديد؟",
                "trigger_date": (datetime.now() + timedelta(days=1)).isoformat() + "Z",
                "status": "pending"
            }
        },
        {
            "reminderId": f"REM{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "reminder_type": "permit_expiry",
                "related_entity_id": "PER456",
                "message": "⚠️ تصريح عمل الموظف أحمد محمد ينتهي خلال 15 يوم. يجب التجديد.",
                "trigger_date": datetime.now().isoformat() + "Z",
                "status": "pending"
            }
        },
        {
            "reminderId": f"REM{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "reminder_type": "certificate_ready",
                "related_entity_id": "CERT789",
                "message": "✅ شهادة الراتب المطلوبة للتأشيرة جاهزة للتحميل!",
                "trigger_date": (datetime.now() - timedelta(days=1)).isoformat() + "Z",
                "status": "pending"
            }
        },
        {
            "reminderId": f"REM{str(uuid.uuid4())[:8].upper()}",
            "data": {
                "reminder_type": "custom",
                "related_entity_id": None,
                "message": "📋 تذكير: تحديث بياناتك الشخصية في منصة قوى",
                "trigger_date": (datetime.now() + timedelta(days=7)).isoformat() + "Z",
                "status": "pending"
            }
        }
    ]
    
    for reminder in reminders:
        reminder_storage.save_reminder(MOCK_USER_ID, reminder["reminderId"], reminder["data"])
        print(f"✅ Added reminder: {reminder['reminderId']} - {reminder['data']['reminder_type']}")
    
    print(f"✅ Total reminders added: {len(reminders)}")

def main():
    """Seed all demo data."""
    print("=" * 60)
    print("🌱 SEEDING DEMO DATA FOR AGENTX")
    print("=" * 60)
    
    seed_contracts()
    seed_certificates()
    seed_work_permits()
    seed_reminders()
    
    print("\n" + "=" * 60)
    print("✅ ALL DEMO DATA SEEDED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📊 Summary:")
    print("  - Contracts: 2")
    print("  - Certificates: 3 (ready, processing, requested)")
    print("  - Work Permits: 5 (2 expiring soon, 1 expired)")
    print("  - Reminders: 4 (contract, permit, certificate, custom)")
    print("\n🎉 Now open the dashboard to see them!")
    print("   http://localhost:5173/dashboard")
    print("=" * 60)

if __name__ == "__main__":
    main()


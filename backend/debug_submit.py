import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api"

def debug_submit():
    # 1. First, create a valid consent in DB
    from app.database import SessionLocal
    from app.models.consent import Consent
    from app.models.organization import Organization
    from app.security import hash_sensitive_data
    from datetime import datetime
    
    db = SessionLocal()
    cnpj = "15.436.940/0001-03"
    cpf = "12345678900"
    
    try:
        org_hash = hash_sensitive_data(cnpj)
        org = db.query(Organization).filter(Organization.cnpj_hash == org_hash).first()
        
        if not org:
            print("❌ Organization not found for test!")
            return

        respondent_hash = hash_sensitive_data(cpf)
        
        # Check/Create consent
        consent = db.query(Consent).filter(Consent.respondent_hash == respondent_hash).first()
        if not consent:
            print(f"Creating Consent for:")
            print(f"  Org ID: {org.id}")
            print(f"  Resp Hash: {respondent_hash}")
            
            consent = Consent(
                respondent_hash=respondent_hash,
                organization_id=org.id,
                consent_version="1.0",
                ip_address="127.0.0.1",
                user_agent="DebugScript",
                accepted_at=datetime.now()
            )
            db.add(consent)
            db.commit()
            print("CREATED test consent")
        else:
            print(f"Consent found for hash: {respondent_hash}")
            print(f"  Consent Org ID: {consent.organization_id}")
            print(f"  Expected Org ID: {org.id}")
            
            if consent.organization_id != org.id:
                 print("ORG ID MISMATCH! Creating new consent for correct org")
                 new_consent = Consent(
                    respondent_hash=respondent_hash,
                    organization_id=org.id,
                    consent_version="1.0",
                    ip_address="127.0.0.1", 
                    user_agent="DebugScript",
                    accepted_at=datetime.now()
                 )
                 db.add(new_consent)
                 db.commit()
                 print("CREATED new consent for correct org")
            
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        db.close()
    
    # 2. We assume consent exists or we might fail with 403, but we want to see if we hit 500
    # Actually, if we use a random CPF, we might hit 403 Consent not found. 
    # But the user is hitting 500, meaning they passed validations.
    
    # Let's try to simulate the exact payload structure
    answers = {str(i): 5 for i in range(1, 94)} # 93 questions
    
    payload = {
        "cpf": cpf,
        "cnpj": cnpj,
        "department_id": None,
        "answers": answers,
        "session_id": str(uuid.uuid4())
    }
    
    print("Sending payload...")
    try:
        resp = requests.post(f"{BASE_URL}/responses/submit", json=payload)
        
        print(f"Response Code: {resp.status_code}")
        
        with open("error_trace.log", "w", encoding="utf-8") as f:
            f.write(resp.text)
            
        print("Logged response to error_trace.log")
            
    except Exception as e:
        print(f"Script error: {e}")

if __name__ == "__main__":
    debug_submit()

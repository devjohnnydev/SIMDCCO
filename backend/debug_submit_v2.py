import requests
import json
import uuid
import random

BASE_URL = "http://localhost:8000/api"

def debug_submit():
    # Generate random CPF to avoid collision
    cpf = "".join([str(random.randint(0, 9)) for _ in range(11)])
    cnpj = "15.436.940/0001-03"
    
    # We need a valid campaign slug. 
    # Let's assume the user has one. I'll fetch campaigns first.
    print("Fetching campaigns...")
    # Login first
    login_data = {"username": "admin@simdcco.com", "password": "admin123"}
    token_resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    token = token_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    camp_resp = requests.get(f"{BASE_URL}/campaigns/", headers=headers)
    campaigns = camp_resp.json()
    
    if not campaigns:
        print("❌ No campaigns found!")
        return
        
    slug = campaigns[0]["slug"]
    print(f"Using campaign slug: {slug}")
    
    # Create consent
    print("Creating consent (bypassing API)...")
    from app.database import SessionLocal
    from app.models.consent import Consent
    from app.models.organization import Organization
    from app.security import hash_sensitive_data
    from datetime import datetime
    
    db = SessionLocal()
    try:
        org_hash = hash_sensitive_data(cnpj)
        org = db.query(Organization).filter(Organization.cnpj_hash == org_hash).first()
        resp_hash = hash_sensitive_data(cpf)
        
        consent = Consent(
            respondent_hash=resp_hash,
            organization_id=org.id,
            consent_version="1.0",
            ip_address="127.0.0.1",
            accepted_at=datetime.utcnow()
        )
        db.add(consent)
        db.commit()
    except Exception as e:
        print(f"Consent error: {e}")
    finally:
        db.close()

    answers = {str(i): 5 for i in range(1, 94)}
    
    payload = {
        "cpf": cpf,
        "cnpj": cnpj,
        "department_id": None,
        "answers": answers,
        "session_id": str(uuid.uuid4()),
        "campaign_slug": slug
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

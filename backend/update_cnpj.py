from app.database import SessionLocal
from app.models.organization import Organization
from app.security import hash_sensitive_data

def update_cnpj():
    db = SessionLocal()
    try:
        # Get the existing organization
        org = db.query(Organization).first()
        if not org:
            print("❌ No organization found to update!")
            return

        print(f"Found organization: {org.razao_social}")
        
        # New CNPJ from user screenshot
        new_cnpj = "15.436.940/0001-03"
        new_hash = hash_sensitive_data(new_cnpj)
        
        org.cnpj_hash = new_hash
        db.commit()
        
        print(f"✅ Updated CNPJ to: {new_cnpj}")
        print("Now the test should work with this CNPJ!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_cnpj()

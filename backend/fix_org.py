from app.database import SessionLocal
from app.models.user import User
from app.models.organization import Organization
from app.security import hash_sensitive_data
import uuid

def fix_admin_org():
    db = SessionLocal()
    try:
        # Get admin user
        user = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if not user:
            print("❌ Admin user not found!")
            return

        print(f"Found user: {user.email}")
        
        # Check if organization exists
        org_cnpj = "00.000.000/0001-91"
        org_hash = hash_sensitive_data(org_cnpj)
        
        org = db.query(Organization).filter(Organization.cnpj_hash == org_hash).first()
        
        if not org:
            print("Creating default organization...")
            org = Organization(
                cnpj_hash=org_hash,
                razao_social="Minha Empresa Demo",
                nome_fantasia="Demo Ltd"
            )
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created organization: {org.razao_social}")
        else:
            print(f"Found existing organization: {org.razao_social}")
            
        # Associate user with organization
        if not user.organization_id:
            user.organization_id = org.id
            db.commit()
            print(f"✅ Associated admin with organization ID: {org.id}")
        else:
            print(f"User already associated with organization ID: {user.organization_id}")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin_org()

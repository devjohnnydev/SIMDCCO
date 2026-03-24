from app.database import SessionLocal
from app.models.user import User

def verify_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if user:
            print(f"User: {user.email}")
            print(f"Organization ID: {user.organization_id}")
            if user.organization_id:
                print("✅ User is associated with an organization.")
            else:
                print("❌ User is NOT associated with any organization.")
        else:
            print("❌ User not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_admin()

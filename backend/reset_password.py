import sys
import os
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

def reset_admin_password():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if user:
            print(f"Found user: {user.email}")
            user.password_hash = hash_password("admin123")
            db.commit()
            print("✅ Password reset to 'admin123' successfully!")
        else:
            print("⚠️ User not found. Creating admin user...")
            new_user = User(
                email="admin@simdcco.com",
                password_hash=hash_password("admin123"),
                name="Administrador",
                role="admin",
                is_active=True
            )
            db.add(new_user)
            db.commit()
            print("✅ Admin user created successfully!")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()

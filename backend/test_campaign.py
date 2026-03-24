from app.database import SessionLocal
from app.models.user import User
from app.models.campaign import Campaign
from datetime import datetime
import secrets

def test_campaign():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if not user or not user.organization_id:
            print("❌ User or organization not found")
            return
            
        print(f"Creating campaign for org: {user.organization_id}")
        
        new_campaign = Campaign(
            organization_id=user.organization_id,
            name="Test Campaign CLI",
            description="Created via CLI",
            slug=secrets.token_urlsafe(16),
            start_date=datetime.now(),
            end_date=None,
            is_active=True,
            created_by=user.id
        )
        
        db.add(new_campaign)
        db.commit()
        print("✅ Campaign created successfully via DB!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_campaign()

from app.database import SessionLocal
from app.models.user import User
from app.models.campaign import Campaign
from app.models.response import Response

def test_list_campaigns():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@simdcco.com").first()
        if not user or not user.organization_id:
            print("❌ User or organization not found")
            return
            
        print(f"Fetching campaigns for org: {user.organization_id}")
        
        campaigns = db.query(Campaign).filter(
            Campaign.organization_id == user.organization_id
        ).all()
        
        print(f"Found {len(campaigns)} campaigns")
        
        for camp in campaigns:
            print(f"Campaign: {camp.name} ({camp.id})")
            print(f"  Created: {camp.created_at}")
            
            # Test response relationship
            response_count = db.query(Response).filter(Response.campaign_id == camp.id).count()
            print(f"  Responses: {response_count}")
            
        print("✅ List campaigns success!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_list_campaigns()

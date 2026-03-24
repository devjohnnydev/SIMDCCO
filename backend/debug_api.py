import requests
import json

BASE_URL = "http://localhost:8000/api"

def debug_api():
    # 1. Login
    print("Logging in...")
    login_data = {
        "username": "admin@simdcco.com",
        "password": "admin123"
    }
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if resp.status_code != 200:
            print(f"❌ Login failed: {resp.status_code} - {resp.text}")
            return
            
        token = resp.json()["access_token"]
        print("✅ Login successful")
        
        # 2. Create Campaign
        print("Attempting to create campaign...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        campaign_data = {
            "name": "Debug Campaign",
            "description": "Debugging 500 error",
            "start_date": "2026-01-25T00:00:00.000Z",
            "end_date": None
        }
        
        resp = requests.post(f"{BASE_URL}/campaigns/", json=campaign_data, headers=headers)
        
        print(f"Detailed Response Code: {resp.status_code}")
        print("Response Body:")
        try:
            print(json.dumps(resp.json(), indent=2))
        except:
            print(resp.text)
            
    except Exception as e:
        print(f"❌ Script error: {e}")

if __name__ == "__main__":
    debug_api()

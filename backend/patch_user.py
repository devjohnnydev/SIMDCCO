import sqlite3

db_path = "c:\\Users\\User\\SIMDCCO\\backend\\simdcco.db"
target_org = "7877dff7-efda-4079-b638-129a580e1f17" # The Org ID from error log
hash_prefix = "ba1e3517"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print(f"Looking for consent with hash starting with {hash_prefix}...")
    cursor.execute("SELECT id, organization_id, respondent_hash FROM consents WHERE respondent_hash LIKE ?", (hash_prefix + '%',))
    row = cursor.fetchone()
    
    if row:
        print(f"Found consent: {row[0]}")
        print(f"Current Org: {row[1]}")
        print(f"Full Hash: {row[2]}")
        
        # Update organization_id to the target one
        print(f"Updating Org ID to {target_org}...")
        cursor.execute("UPDATE consents SET organization_id = ? WHERE id = ?", (target_org, row[0]))
        conn.commit()
        print("✅ Successfully updated consent organization!")
    else:
        print("❌ No matching consent found.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()

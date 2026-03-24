import sqlite3

db_path = "c:\\Users\\User\\SIMDCCO\\backend\\simdcco.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Dropping unique index...")
    cursor.execute("DROP INDEX IF EXISTS ix_consents_respondent_hash")
    
    print("Creating non-unique index...")
    cursor.execute("CREATE INDEX ix_consents_respondent_hash ON consents(respondent_hash)")
    
    conn.commit()
    print("✅ Successfully removed unique constraint on respondent_hash!")
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()

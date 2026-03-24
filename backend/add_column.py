import sqlite3

def add_column():
    print("Migrating database...")
    try:
        conn = sqlite3.connect("simdcco.db")
        cursor = conn.cursor()
        
        # Check if column exists strictly (though error says no)
        cursor.execute("PRAGMA table_info(responses)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "campaign_id" not in columns:
            print("Adding campaign_id column...")
            # SQLite add column validation
            cursor.execute("ALTER TABLE responses ADD COLUMN campaign_id CHAR(32)")
            conn.commit()
            print("✅ Column added successfully")
        else:
            print("Column already exists (unexpected)")
            
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_column()

import sqlite3
import os

# Path to db
db_path = "c:\\Users\\User\\SIMDCCO\\backend\\simdcco.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Indices on consents table:")
cursor.execute("PRAGMA index_list('consents')")
indices = cursor.fetchall()
for idx in indices:
    print(idx)
    # idx: (seq, name, unique, origin, partial)
    if idx[2] == 1: # Unique
        print(f" -> Found unique index: {idx[1]}")
        # Check columns
        cursor.execute(f"PRAGMA index_info('{idx[1]}')")
        cols = cursor.fetchall()
        for col in cols:
             print(f"    Column: {col[2]}")

conn.close()

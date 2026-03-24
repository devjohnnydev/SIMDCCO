import sqlite3

def check_schema():
    conn = sqlite3.connect("simdcco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='responses'")
    print(cursor.fetchone()[0])
    conn.close()

if __name__ == "__main__":
    check_schema()

import sqlite3
import pandas as pd

db_path = "c:\\Users\\User\\SIMDCCO\\backend\\simdcco.db"

conn = sqlite3.connect(db_path)

print("--- ORGANIZATIONS ---")
orgs = pd.read_sql_query("SELECT id, razao_social, substr(cnpj_hash, 1, 10) as hash_preview FROM organizations", conn)
print(orgs)

print("\n--- CONSENTS ---")
consents = pd.read_sql_query("SELECT id, organization_id, substr(respondent_hash, 1, 10) as hash_preview, accepted_at FROM consents", conn)
print(consents)

print("\n--- CAMPAIGNS ---")
campaigns = pd.read_sql_query("SELECT id, name, slug, organization_id FROM campaigns", conn)
print(campaigns)

conn.close()

from passlib.context import CryptContext

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print("Hashing 'admin123'...")
    hashed = pwd_context.hash("admin123")
    print(f"Success! Hash: {hashed}")
except Exception as e:
    print(f"Error: {e}")

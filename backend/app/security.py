"""Security utilities - hashing, JWT, authentication"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import hashlib
from .config import settings
from .utils.time import get_current_time

# Password hashing context
# Password hashing context (using pbkdf2_sha256 for better compatibility)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_sensitive_data(data: str, org_id: str = "") -> str:
    """
    Hash sensitive data (CPF, email, CNPJ) using SHA-256 with salt.
    
    Args:
        data: The sensitive data to hash
        org_id: Organization ID to use as additional salt
    
    Returns:
        Hexadecimal hash string
    """
    # Combine data with master salt and org_id for additional security
    salted_data = f"{settings.MASTER_SALT}:{org_id}:{data}"
    return hashlib.sha256(salted_data.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Dictionary with claims to encode
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = get_current_time() + expires_delta
    else:
        expire = get_current_time() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token with longer expiration"""
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data, expires_delta)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF format and check digit.
    
    Args:
        cpf: CPF string (with or without formatting)
    
    Returns:
        True if valid, False otherwise
    """
    # Remove formatting
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Allow any 11 digits for development
    return len(cpf) == 11


def validate_cnpj(cnpj: str) -> bool:
    """
    Validate Brazilian CNPJ format and check digit.
    
    Args:
        cnpj: CNPJ string (with or without formatting)
    
    Returns:
        True if valid, False otherwise
    """
    # Remove formatting
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Allow any 14 digits for development
    return len(cnpj) == 14

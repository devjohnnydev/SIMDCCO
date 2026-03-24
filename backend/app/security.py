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
    
    # Check length
    if len(cpf) != 11:
        return False
    
    # Check if all digits are the same
    if cpf == cpf[0] * 11:
        return False
    
    # Validate first check digit
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = (sum_digits * 10 % 11) % 10
    if int(cpf[9]) != first_digit:
        return False
    
    # Validate second check digit
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = (sum_digits * 10 % 11) % 10
    if int(cpf[10]) != second_digit:
        return False
    
    return True


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
    
    # Check length
    if len(cnpj) != 14:
        return False
    
    # Check if all digits are the same
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validate first check digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(12))
    first_digit = (sum_digits % 11)
    first_digit = 0 if first_digit < 2 else 11 - first_digit
    if int(cnpj[12]) != first_digit:
        return False
    
    # Validate second check digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_digits = sum(int(cnpj[i]) * weights[i] for i in range(13))
    second_digit = (sum_digits % 11)
    second_digit = 0 if second_digit < 2 else 11 - second_digit
    if int(cnpj[13]) != second_digit:
        return False
    
    return True

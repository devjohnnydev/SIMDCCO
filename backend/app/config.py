"""Application Configuration"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Info
    APP_NAME: str = "SIMDCCO"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database (SQLite for local development, PostgreSQL for production)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./simdcco.db")
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ]
    
    # SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Reports
    REPORTS_DIR: str = "./reports"
    
    
    # Hash Salt (per organization - this is the master salt)
    MASTER_SALT: str = "simdcco-master-salt-change-in-production"
    
    # System Timezone
    TIMEZONE: str = "America/Sao_Paulo"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Create reports directory if doesn't exist
os.makedirs(settings.REPORTS_DIR, exist_ok=True)

"""Database configuration and session management"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Use this in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    from .models import (
        organization, user, department, consent, 
        question, response, report, analytic, 
        audit_log, lgpd_deletion
    )
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def drop_db():
    """Drop all database tables - USE WITH CAUTION!"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Database dropped!")

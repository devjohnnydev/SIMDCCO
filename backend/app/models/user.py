"""User model - Admin, RH, Juridico"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid
import enum

from ..database import Base


class UserRole(str, enum.Enum):
    """User roles in the system"""
    ADMIN = "admin"
    RH = "rh"
    JURIDICO = "juridico"
    CEO = "ceo"


class User(Base):
    """
    System users (administrators, HR, legal team).
    Not the respondents - those are anonymous.
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.RH)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    mfa_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    approved_reports = relationship("Report", back_populates="approver", foreign_keys="Report.approved_by")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role.value})>"

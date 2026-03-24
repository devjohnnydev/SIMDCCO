"""Organization model"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..utils.time import get_current_time

from ..database import Base


class Organization(Base):
    """
    Organization/Company entity.
    Stores companies that use the SIMDCCO system.
    """
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj_hash = Column(String(64), unique=True, nullable=False, index=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time, nullable=False)
    
    # Relationships
    departments = relationship("Department", back_populates="organization", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="organization", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="organization")
    reports = relationship("Report", back_populates="organization")
    analytics = relationship("Analytic", back_populates="organization")
    users = relationship("User", back_populates="organization")
    consents = relationship("Consent", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization {self.razao_social}>"

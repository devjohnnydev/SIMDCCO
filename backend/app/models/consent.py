"""Consent model - LGPD compliance"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..utils.time import get_current_time

from ..database import Base


class Consent(Base):
    """
    LGPD consent records.
    Stores user consent with timestamp, IP, and user agent for legal proof.
    """
    __tablename__ = "consents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    respondent_hash = Column(String(64), nullable=False, unique=True, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    consent_version = Column(String(50), nullable=False)  # e.g., "1.0"
    ip_address = Column(String(45), nullable=False)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    accepted_at = Column(DateTime, default=get_current_time, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="consents")
    responses = relationship("Response", back_populates="consent")
    
    def __repr__(self):
        return f"<Consent {self.respondent_hash[:8]}... v{self.consent_version}>"

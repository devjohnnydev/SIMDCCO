"""Response model - Survey responses"""
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid

from ..database import Base


class Response(Base):
    """
    Survey responses from respondents.
    Stores answers in JSONB format: {question_id: value (1-5)}
    """
    __tablename__ = "responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    respondent_hash = Column(String(64), nullable=False, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=True)
    consent_id = Column(UUID(as_uuid=True), ForeignKey("consents.id"), nullable=False)
    
    # Answers stored as JSON: {"1": 5, "2": 3, "3": 4, ...}
    answers = Column(JSON, nullable=False)
    
    # Session tracking
    session_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    started_at = Column(DateTime, default=get_current_time, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="responses")
    department = relationship("Department", back_populates="responses")
    campaign = relationship("Campaign", back_populates="responses")
    consent = relationship("Consent", back_populates="responses")
    
    # Ensure one response per respondent per organization
    __table_args__ = (
        UniqueConstraint('respondent_hash', 'organization_id', name='uq_respondent_organization'),
    )
    
    def __repr__(self):
        return f"<Response {self.id} - {self.respondent_hash[:8]}...>"

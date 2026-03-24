"""Campaign model - Diagnostic campaigns"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..utils.time import get_current_time

from ..database import Base


class Campaign(Base):
    """
    Diagnostic campaigns for collecting responses.
    Each campaign has a unique link and can be activated/deactivated.
    """
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Campaign details
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Unique campaign link identifier
    slug = Column(String(100), unique=True, nullable=False, index=True)
    
    # Campaign period
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    responses = relationship("Response", back_populates="campaign")
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Campaign {self.name} - {self.slug}>"

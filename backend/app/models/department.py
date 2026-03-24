"""Department model"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid

from ..database import Base


class Department(Base):
    """
    Department/Sector within an organization.
    Used for segmented analysis.
    """
    __tablename__ = "departments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="departments")
    responses = relationship("Response", back_populates="department")
    analytics = relationship("Analytic", back_populates="department")
    
    def __repr__(self):
        return f"<Department {self.name}>"

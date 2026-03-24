"""Audit Log model - Immutable audit trail"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid

from ..database import Base


class AuditLog(Base):
    """
    Immutable audit log for all critical actions.
    Never delete - only insert.
    """
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Who did it (nullable for anonymous actions)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # What action was performed
    action = Column(String(255), nullable=False, index=True)
    
    # Entity affected
    entity_type = Column(String(100), nullable=False)  # e.g., "Response", "Report"
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Details of changes (before/after)
    changes = Column(JSON, nullable=True)
    
    # Request metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # When it happened
    timestamp = Column(DateTime, default=get_current_time, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type}>"

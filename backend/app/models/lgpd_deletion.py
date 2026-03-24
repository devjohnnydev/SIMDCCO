"""LGPD Deletion model - Track data deletion requests"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..utils.time import get_current_time
import uuid

from ..database import Base


class LGPDDeletion(Base):
    """
    Track LGPD data deletion requests.
    Maintains record of deletion without storing personal data.
    """
    __tablename__ = "lgpd_deletions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Hash of deleted respondent (we keep hash for audit trail)
    respondent_hash = Column(String(64), nullable=False, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Timestamps
    requested_at = Column(DateTime, default=get_current_time, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Who executed the deletion
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    def __repr__(self):
        return f"<LGPDDeletion {self.respondent_hash[:8]}... at {self.deleted_at}>"

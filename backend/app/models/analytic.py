"""Analytic model - Calculated metrics and risk assessments"""
from sqlalchemy import Column, String, DateTime, Integer, Date, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid
import enum

from ..database import Base


class RiskLevel(str, enum.Enum):
    """Psychosocial risk level"""
    LOW = "low"  # Score >= 4.0
    MEDIUM = "medium"  # Score >= 3.0
    HIGH = "high"  # Score < 3.0
    CRITICAL = "critical"  # Score < 2.0


class Analytic(Base):
    """
    Pre-calculated analytics and metrics.
    Stored for performance and historical tracking.
    """
    __tablename__ = "analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    
    # Time period for this analysis
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Scores stored as JSON
    # IMCO: {"vectors": {...}, "dimensions": {...}, "overall": 3.5}
    # FDAC: {"dimensions": {...}, "overall": 3.2}
    imco_scores = Column(JSON, nullable=False)
    fdac_scores = Column(JSON, nullable=False)
    
    # Risk assessment
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    
    # Statistics
    respondent_count = Column(Integer, nullable=False)
    
    # Calculation metadata
    calculated_at = Column(DateTime, default=get_current_time, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="analytics")
    department = relationship("Department", back_populates="analytics")
    
    def __repr__(self):
        return f"<Analytic {self.organization_id} - {self.risk_level.value}>"

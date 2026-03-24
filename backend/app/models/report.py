"""Report model - Generated reports and technical opinions"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..utils.time import get_current_time
import uuid
import enum

from ..database import Base


class ReportType(str, enum.Enum):
    """Type of report"""
    INDIVIDUAL = "individual"  # For respondent
    DEPARTMENTAL = "departmental"  # For department
    ORGANIZATIONAL = "organizational"  # For entire organization
    NR01_COMPLIANCE = "nr01_compliance"  # NR-01 compliance report


class ReportStatus(str, enum.Enum):
    """Report approval status"""
    PENDING = "pending"
    APPROVED = "approved"
    SENT = "sent"


class Report(Base):
    """
    Generated reports and technical opinions.
    Has unique numbering for legal traceability.
    """
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Unique report number: SIMDCCO-2026-00001
    report_number = Column(String(50), unique=True, nullable=False, index=True)
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    
    # Target (respondent hash or department id depending on type)
    target_id = Column(String(255), nullable=True)
    
    # PDF file path
    pdf_path = Column(String(500), nullable=True)
    
    # Versioning for reports
    version = Column(Integer, default=1, nullable=False)
    
    # Timestamps
    generated_at = Column(DateTime, default=get_current_time, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    
    # Approval tracking
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="reports")
    approver = relationship("User", back_populates="approved_reports", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<Report {self.report_number} - {self.report_type.value}>"

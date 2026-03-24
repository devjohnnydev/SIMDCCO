"""Reports routes - Generate and manage reports"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import uuid
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.report import Report, ReportType, ReportStatus
from ..utils.time import get_current_time
from ..models.organization import Organization
from ..routes.auth import get_current_user
from ..services.analytics import calculate_organization_analytics
from ..services.report_generator import report_generator

router = APIRouter()


# Schemas
class ReportGenerate(BaseModel):
    report_type: str
    department_id: str | None = None


class ReportResponse(BaseModel):
    id: str
    report_number: str
    report_type: str
    status: str
    generated_at: str
    pdf_path: str | None
    
    class Config:
        from_attributes = True


# Routes
@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    data: ReportGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new report"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )
    
    # Get organization
    org = db.query(Organization).filter(
        Organization.id == current_user.organization_id
    ).first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Get analytics data
    dept_uuid = uuid.UUID(data.department_id) if data.department_id else None
    analytics = calculate_organization_analytics(current_user.organization_id, dept_uuid, db)
    
    # Generate unique report number
    year = datetime.now().year
    count = db.query(Report).filter(
        Report.organization_id == current_user.organization_id
    ).count() + 1
    report_number = f"SIMDCCO-{year}-{count:05d}"
    
    # Generate PDF
    pdf_path = report_generator.generate_organizational_report(
        organization_name=org.razao_social,
        analytics_data=analytics,
        report_number=report_number
    )
    
    # Create report record
    report = Report(
        report_number=report_number,
        organization_id=current_user.organization_id,
        report_type=ReportType.ORGANIZATIONAL,
        status=ReportStatus.APPROVED,  # Auto-approve for MVP
        target_id=str(data.department_id) if data.department_id else None,
        pdf_path=pdf_path,
        generated_at=get_current_time(),
        approved_at=get_current_time(),
        approved_by=current_user.id
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return ReportResponse(
        id=str(report.id),
        report_number=report.report_number,
        report_type=report.report_type.value,
        status=report.status.value,
        generated_at=report.generated_at.isoformat(),
        pdf_path=report.pdf_path
    )


@router.get("", response_model=List[ReportResponse])
async def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all reports for current user's organization"""
    if not current_user.organization_id:
        return []
    
    reports = db.query(Report).filter(
        Report.organization_id == current_user.organization_id
    ).order_by(Report.generated_at.desc()).all()
    
    return [
        ReportResponse(
            id=str(r.id),
            report_number=r.report_number,
            report_type=r.report_type.value,
            status=r.status.value,
            generated_at=r.generated_at.isoformat(),
            pdf_path=r.pdf_path
        )
        for r in reports
    ]


@router.get("/{report_id}/download")
async def download_report(
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download report PDF"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.organization_id == current_user.organization_id
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if not report.pdf_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not found"
        )
    
    return FileResponse(
        report.pdf_path,
        media_type='application/pdf',
        filename=f"{report.report_number}.pdf"
    )

"""Respondents routes - Survey access and validation"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

from ..database import get_db
from ..models.organization import Organization
from ..models.department import Department
from ..models.consent import Consent
from ..security import hash_sensitive_data, validate_cpf, validate_cnpj
from ..utils.time import get_current_time


router = APIRouter()


# Schemas
class RespondentValidation(BaseModel):
    cpf: str
    email: EmailStr
    cnpj: str
    department_name: str | None = None


class ConsentCreate(BaseModel):
    cpf: str
    cnpj: str
    email: EmailStr
    consent_version: str = "1.0"


class ValidationResponse(BaseModel):
    success: bool
    organization_name: str
    department_id: str | None
    session_id: str


class ConsentResponse(BaseModel):
    success: bool
    consent_id: str
    respondent_hash: str


# Routes
@router.post("/validate")
async def validate_respondent(
    data: RespondentValidation,
    campaign_slug: str = None,
    db: Session = Depends(get_db)
):
    """
    Validate respondent data before starting questionnaire.
    If campaign_slug not provided, uses default public campaign.
    """
    # Validate CPF
    if not validate_cpf(data.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CPF format"
        )
    
    # Validate CNPJ
    if not validate_cnpj(data.cnpj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CNPJ format"
        )
    
    # Find organization
    cnpj_hash = hash_sensitive_data(data.cnpj)
    org = db.query(Organization).filter(
        Organization.cnpj_hash == cnpj_hash
    ).first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found. Please contact your administrator."
        )
    
    # Find or create department
    department_id = None
    if data.department_name:
        dept = db.query(Department).filter(
            Department.organization_id == org.id,
            Department.name == data.department_name
        ).first()
        
        if not dept:
            dept = Department(
                organization_id=org.id,
                name=data.department_name
            )
            db.add(dept)
            db.commit()
            db.refresh(dept)
        
        department_id = str(dept.id)
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    return ValidationResponse(
        success=True,
        organization_name=org.nome_fantasia or org.razao_social,
        department_id=department_id,
        session_id=session_id
    )


@router.post("/consent", response_model=ConsentResponse)
async def register_consent(
    data: ConsentCreate,
    request: Request,
    campaign_slug: str = None,
    db: Session = Depends(get_db)
):
    """
    Register LGPD consent.
    This is required before answering questionnaire.
    If campaign_slug not provided, uses default public campaign.
    """
    # Hash identifiers
    cpf_hash = hash_sensitive_data(data.cpf)
    cnpj_hash = hash_sensitive_data(data.cnpj)
    
    campaign = None
    if campaign_slug:
        campaign = db.query(Campaign).filter(Campaign.slug == campaign_slug).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
    else:
        # Require campaign slug or explicit organization context
        pass
        
    # Get organization
    if campaign:
        organization = db.query(Organization).filter(
            Organization.id == campaign.organization_id
        ).first()
    else:
        # Legacy/Direct flow by CNPJ (if supported) or fail
        # For now, let's look up by CNPJ hash if no campaign provided
        organization = db.query(Organization).filter(
            Organization.cnpj_hash == cnpj_hash
        ).first()
        
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found. Please check CNPJ or Campaign Link."
        )
    
    # Check if consent already exists
    existing_consent = db.query(Consent).filter(
        Consent.respondent_hash == cpf_hash,
        Consent.organization_id == organization.id
    ).first()
    
    if existing_consent:
        return ConsentResponse(
            success=True,
            consent_id=str(existing_consent.id),
            respondent_hash=cpf_hash
        )
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # Create consent record
    consent = Consent(
        respondent_hash=cpf_hash,
        organization_id=organization.id,
        consent_version=data.consent_version,
        ip_address=client_ip,
        user_agent=user_agent,
        accepted_at=get_current_time()
    )
    
    db.add(consent)
    db.commit()
    db.refresh(consent)
    
    return ConsentResponse(
        success=True,
        consent_id=str(consent.id),
        respondent_hash=cpf_hash
    )

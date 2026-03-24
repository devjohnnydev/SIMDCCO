"""LGPD routes - Data deletion and privacy"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..database import get_db
from ..models.user import User
from ..models.response import Response
from ..models.consent import Consent
from ..models.lgpd_deletion import LGPDDeletion
from ..utils.time import get_current_time
from ..routes.auth import get_current_user
from ..security import hash_sensitive_data

router = APIRouter()


# Schemas
class DeleteDataRequest(BaseModel):
    cpf: str
    email: str


class DeleteDataResponse(BaseModel):
    success: bool
    message: str
    deleted_responses: int
    deleted_consents: int


# Routes
@router.post("/delete-data", response_model=DeleteDataResponse)
async def delete_user_data(
    data: DeleteDataRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete all data for a specific respondent (LGPD compliance).
    This is a critical operation that should be used carefully.
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )
    
    # Hash CPF to find respondent
    cpf_hash = hash_sensitive_data(data.cpf)
    
    # Find responses to delete
    responses = db.query(Response).filter(
        Response.respondent_hash == cpf_hash,
        Response.organization_id == current_user.organization_id
    ).all()
    
    response_count = len(responses)
    
    # Find consents to delete
    consents = db.query(Consent).filter(
        Consent.respondent_hash == cpf_hash,
        Consent.organization_id == current_user.organization_id
    ).all()
    
    consent_count = len(consents)
    
    # Delete responses
    for response in responses:
        db.delete(response)
    
    # Delete consents
    for consent in consents:
        db.delete(consent)
    
    # Create deletion record (for audit trail)
    deletion_record = LGPDDeletion(
        respondent_hash=cpf_hash,
        organization_id=current_user.organization_id,
        requested_at=get_current_time(),
        deleted_at=get_current_time(),
        deleted_by=current_user.id
    )
    
    db.add(deletion_record)
    db.commit()
    
    return DeleteDataResponse(
        success=True,
        message=f"Dados excluídos com sucesso. LGPD compliance registrado.",
        deleted_responses=response_count,
        deleted_consents=consent_count
    )


@router.get("/consents")
async def list_consents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all consents for organization"""
    if not current_user.organization_id:
        return []
    
    consents = db.query(Consent).filter(
        Consent.organization_id == current_user.organization_id
    ).order_by(Consent.accepted_at.desc()).limit(100).all()
    
    return [
        {
            "id": str(c.id),
            "respondent_hash": c.respondent_hash[:16] + "...",  # Partial hash for privacy
            "consent_version": c.consent_version,
            "accepted_at": c.accepted_at.isoformat(),
            "ip_address": c.ip_address
        }
        for c in consents
    ]


@router.get("/deletions")
async def list_deletions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all LGPD deletion records"""
    if not current_user.organization_id:
        return []
    
    deletions = db.query(LGPDDeletion).filter(
        LGPDDeletion.organization_id == current_user.organization_id
    ).order_by(LGPDDeletion.deleted_at.desc()).all()
    
    return [
        {
            "id": str(d.id),
            "respondent_hash": d.respondent_hash[:16] + "...",
            "requested_at": d.requested_at.isoformat() if d.requested_at else None,
            "deleted_at": d.deleted_at.isoformat() if d.deleted_at else None
        }
        for d in deletions
    ]

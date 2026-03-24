"""Organizations routes - CRUD for organizations"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.organization import Organization
from ..models.user import User
from ..routes.auth import get_current_user
from ..security import hash_sensitive_data, validate_cnpj


router = APIRouter()


# Schemas
class OrganizationCreate(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: str | None = None


class OrganizationResponse(BaseModel):
    id: str
    razao_social: str
    nome_fantasia: str | None
    created_at: str
    
    class Config:
        from_attributes = True


# Routes
@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new organization"""
    # Validate CNPJ
    if not validate_cnpj(org.cnpj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CNPJ format"
        )
    
    # Hash CNPJ
    cnpj_hash = hash_sensitive_data(org.cnpj)
    
    # Check if already exists
    existing = db.query(Organization).filter(
        Organization.cnpj_hash == cnpj_hash
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization already registered"
        )
    
    # Create organization
    new_org = Organization(
        cnpj_hash=cnpj_hash,
        razao_social=org.razao_social,
        nome_fantasia=org.nome_fantasia
    )
    
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    
    return OrganizationResponse(
        id=str(new_org.id),
        razao_social=new_org.razao_social,
        nome_fantasia=new_org.nome_fantasia,
        created_at=new_org.created_at.isoformat()
    )


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all organizations"""
    orgs = db.query(Organization).all()
    return [
        OrganizationResponse(
            id=str(org.id),
            razao_social=org.razao_social,
            nome_fantasia=org.nome_fantasia,
            created_at=org.created_at.isoformat()
        )
        for org in orgs
    ]


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get organization by ID"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationResponse(
        id=str(org.id),
        razao_social=org.razao_social,
        nome_fantasia=org.nome_fantasia,
        created_at=org.created_at.isoformat()
    )


class OrganizationUpdate(BaseModel):
    razao_social: str | None = None
    nome_fantasia: str | None = None


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: uuid.UUID,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update organization"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Update fields
    if org_update.razao_social is not None:
        org.razao_social = org_update.razao_social
    if org_update.nome_fantasia is not None:
        org.nome_fantasia = org_update.nome_fantasia
    
    db.commit()
    db.refresh(org)
    
    return OrganizationResponse(
        id=str(org.id),
        razao_social=org.razao_social,
        nome_fantasia=org.nome_fantasia,
        created_at=org.created_at.isoformat()
    )


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete organization"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    db.delete(org)
    db.commit()
    
    return None

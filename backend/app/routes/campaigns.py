"""Campaign routes - Create and manage diagnostic campaigns"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid
import secrets

from ..database import get_db
from ..models.campaign import Campaign
from ..models.user import User
from ..routes.auth import get_current_user


router = APIRouter()


# Schemas
class CampaignCreate(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime
    end_date: datetime | None = None
    organization_id: uuid.UUID | None = None


class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None


class CampaignResponse(BaseModel):
    id: str
    name: str
    description: str | None
    slug: str
    link: str
    start_date: str
    end_date: str | None
    is_active: bool
    created_at: str
    response_count: int = 0
    
    class Config:
        from_attributes = True


# Routes
@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Determine organization ID
    print(f"DEBUG: Creating campaign for user {current_user.email} (Org: {current_user.organization_id})")
    org_id = campaign.organization_id or current_user.organization_id
    print(f"DEBUG: Initial org_id: {org_id}")
    
    if not org_id:
        # If Admin, try to find any organization to associate with
        from ..models.user import UserRole
        if current_user.role == UserRole.ADMIN:
            from ..models.organization import Organization
            first_org = db.query(Organization).first()
            if first_org:
                org_id = first_org.id
                print(f"DEBUG: Admin fallback to first org_id: {org_id}")
        
    if not org_id:
        print("DEBUG: No organization found for campaign")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhuma organização encontrada. Crie uma organização primeiro."
        )
    
    # Generate unique slug
    slug = secrets.token_urlsafe(16)
    print(f"DEBUG: Generated slug: {slug}")
    
    try:
        # Create campaign
        print(f"DEBUG: Instantiating Campaign model for {campaign.name}")
        new_campaign = Campaign(
            organization_id=org_id,
            name=campaign.name,
            description=campaign.description,
            slug=slug,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            is_active=True,
            created_by=current_user.id
        )
        
        print(f"DEBUG: Adding campaign to DB: {new_campaign.name}")
        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)
        print(f"DEBUG: Campaign created successfully: {new_campaign.id}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        print(f"DEBUG: Campaign creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar campanha: {str(e)}"
        )
    
    # Get response count (safely)
    try:
        from ..models.response import Response
        response_count = db.query(Response).filter(Response.campaign_id == new_campaign.id).count()
    except Exception:
        response_count = 0
    
    return CampaignResponse(
        id=str(new_campaign.id),
        name=new_campaign.name,
        description=new_campaign.description,
        slug=new_campaign.slug,
        link=f"/respondent?c={new_campaign.slug}",
        start_date=new_campaign.start_date.isoformat(),
        end_date=new_campaign.end_date.isoformat() if new_campaign.end_date else None,
        is_active=new_campaign.is_active,
        created_at=new_campaign.created_at.isoformat(),
        response_count=response_count
    )


@router.get("", response_model=List[CampaignResponse])
async def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all campaigns for current user's organization"""
    if not current_user.organization_id:
        return []
    
    campaigns = db.query(Campaign).filter(
        Campaign.organization_id == current_user.organization_id
    ).order_by(Campaign.created_at.desc()).all()
    
    # Get response counts
    from ..models.response import Response
    result = []
    for camp in campaigns:
        try:
            response_count = db.query(Response).filter(Response.campaign_id == camp.id).count()
        except Exception:
            response_count = 0
            
        result.append(CampaignResponse(
            id=str(camp.id),
            name=camp.name,
            description=camp.description,
            slug=camp.slug,
            link=f"/respondent?c={camp.slug}",
            start_date=camp.start_date.isoformat(),
            end_date=camp.end_date.isoformat() if camp.end_date else None,
            is_active=camp.is_active,
            created_at=camp.created_at.isoformat(),
            response_count=response_count
        ))
   
    return result


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get campaign by ID"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    from ..models.response import Response
    response_count = db.query(Response).filter(Response.campaign_id == campaign.id).count()
    
    return CampaignResponse(
        id=str(campaign.id),
        name=campaign.name,
        description=campaign.description,
        slug=campaign.slug,
        link=f"/respondent?c={campaign.slug}",
        start_date=campaign.start_date.isoformat(),
        end_date=campaign.end_date.isoformat() if campaign.end_date else None,
        is_active=campaign.is_active,
        created_at=campaign.created_at.isoformat(),
        response_count=response_count
    )


@router.patch("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: uuid.UUID,
    updates: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update campaign"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Update fields
    if updates.name is not None:
        campaign.name = updates.name
    if updates.description is not None:
        campaign.description = updates.description
    if updates.start_date is not None:
        campaign.start_date = updates.start_date
    if updates.end_date is not None:
        campaign.end_date = updates.end_date
    if updates.is_active is not None:
        campaign.is_active = updates.is_active
    
    db.commit()
    db.refresh(campaign)
    
    from ..models.response import Response
    response_count = db.query(Response).filter(Response.campaign_id == campaign.id).count()
    
    return CampaignResponse(
        id=str(campaign.id),
        name=campaign.name,
        description=campaign.description,
        slug=campaign.slug,
        link=f"/respondent?c={campaign.slug}",
        start_date=campaign.start_date.isoformat(),
        end_date=campaign.end_date.isoformat() if campaign.end_date else None,
        is_active=campaign.is_active,
        created_at=campaign.created_at.isoformat(),
        response_count=response_count
    )


@router.post("/{campaign_id}/toggle")
async def toggle_campaign(
    campaign_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle campaign active status"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.organization_id == current_user.organization_id
    ).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.is_active = not campaign.is_active
    db.commit()
    
    return {"success": True, "is_active": campaign.is_active}

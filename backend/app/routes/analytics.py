"""Analytics routes - Get calculated analytics"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from ..database import get_db
from ..models.user import User
from ..routes.auth import get_current_user
from ..services.analytics import calculate_organization_analytics, save_analytics
from datetime import date

router = APIRouter()


@router.get("/organization")
async def get_organization_analytics(
    department_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics for organization or specific department"""
    if not current_user.organization_id:
        return {"error": "User not associated with organization"}
    
    dept_uuid = uuid.UUID(department_id) if department_id else None
    
    analytics = calculate_organization_analytics(
        current_user.organization_id,
        dept_uuid,
        db
    )
    
    return analytics


@router.post("/calculate")
async def calculate_and_save_analytics(
    department_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate and save analytics snapshot"""
    if not current_user.organization_id:
        return {"error": "User not associated with organization"}
    
    dept_uuid = uuid.UUID(department_id) if department_id else None
    
    analytic = save_analytics(
        current_user.organization_id,
        dept_uuid,
        date.today(),
        date.today(),
        db
    )
    
    return {
        "id": str(analytic.id),
        "respondent_count": analytic.respondent_count,
        "imco_scores": analytic.imco_scores,
        "fdac_scores": analytic.fdac_scores,
        "risk_level": analytic.risk_level.value
    }

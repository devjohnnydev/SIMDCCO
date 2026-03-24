"""Campaign analytics - Detailed analysis per campaign"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models.campaign import Campaign
from ..models.response import Response
from ..models.department import Department
from ..models.user import User
from ..routes.auth import get_current_user
from ..services.analytics import calculate_imco_scores, calculate_fdac_scores


router = APIRouter()


# Schemas
class ResponseDetail(BaseModel):
    id: str
    department_name: str | None
    completed_at: str
    imco_overall: float
    fdac_overall: float


class DepartmentStats(BaseModel):
    department_name: str
    response_count: int
    imco_average: float
    fdac_average: float


class CampaignAnalytics(BaseModel):
    campaign_id: str
    campaign_name: str
    total_responses: int
    completion_rate: float
    
    # IMCO Scores
    imco_overall: float
    imco_vectors: Dict[str, float]
    imco_dimensions: Dict[str, float]
    
    # FDAC Scores
    fdac_overall: float
    fdac_dimensions: Dict[str, float]
    
    # Breakdown
    department_stats: List[DepartmentStats]
    recent_responses: List[ResponseDetail]


# Routes
@router.get("/{campaign_id}", response_model=CampaignAnalytics)
async def get_campaign_analytics(
    campaign_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive analytics for a specific campaign.
    Includes IMCO/FDAC scores, department breakdown, and recent responses.
    """
    # Get campaign
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Get all responses for this campaign
    responses = db.query(Response).filter(
        Response.campaign_id == campaign_id,
        Response.completed_at.isnot(None)
    ).all()
    
    total_responses = len(responses)
    
    if total_responses == 0:
        return CampaignAnalytics(
            campaign_id=str(campaign.id),
            campaign_name=campaign.name,
            total_responses=0,
            completion_rate=0.0,
            imco_overall=0.0,
            imco_vectors={},
            imco_dimensions={},
            fdac_overall=0.0,
            fdac_dimensions={},
            department_stats=[],
            recent_responses=[]
        )
    
    # Aggregate IMCO and FDAC scores
    all_imco_vectors = {}
    all_imco_dimensions = {}
    all_fdac_dimensions = {}
    all_imco_overalls = []
    all_fdac_overalls = []
    
    # Department-wise aggregation
    dept_responses = {}  # {dept_id: [responses]}
    
    for response in responses:
        # Calculate individual scores
        imco = calculate_imco_scores(response.answers, db)
        fdac = calculate_fdac_scores(response.answers, db)
        
        all_imco_overalls.append(imco['overall'])
        all_fdac_overalls.append(fdac['overall'])
        
        # Aggregate IMCO vectors
        for vector, score in imco['vectors'].items():
            if vector not in all_imco_vectors:
                all_imco_vectors[vector] = []
            all_imco_vectors[vector].append(score)
        
        # Aggregate IMCO dimensions
        for dimension, score in imco['dimensions'].items():
            if dimension not in all_imco_dimensions:
                all_imco_dimensions[dimension] = []
            all_imco_dimensions[dimension].append(score)
        
        # Aggregate FDAC dimensions
        for dimension, score in fdac['dimensions'].items():
            if dimension not in all_fdac_dimensions:
                all_fdac_dimensions[dimension] = []
            all_fdac_dimensions[dimension].append(score)
        
        # Group by department
        dept_id = str(response.department_id) if response.department_id else "undefined"
        if dept_id not in dept_responses:
            dept_responses[dept_id] = []
        dept_responses[dept_id].append({
            'imco': imco['overall'],
            'fdac': fdac['overall']
        })
    
    # Calculate campaign-wide averages
    imco_overall = round(sum(all_imco_overalls) / len(all_imco_overalls), 2)
    fdac_overall = round(sum(all_fdac_overalls) / len(all_fdac_overalls), 2)
    
    imco_vectors_avg = {
        v: round(sum(scores) / len(scores), 2) 
        for v, scores in all_imco_vectors.items()
    }
    
    imco_dimensions_avg = {
        d: round(sum(scores) / len(scores), 2) 
        for d, scores in all_imco_dimensions.items()
    }
    
    fdac_dimensions_avg = {
        d: round(sum(scores) / len(scores), 2) 
        for d, scores in all_fdac_dimensions.items()
    }
    
    # Calculate department stats
    department_stats = []
    for dept_id, dept_data in dept_responses.items():
        if dept_id == "undefined":
            dept_name = "Sem Departamento"
        else:
            dept = db.query(Department).filter(
                Department.id == uuid.UUID(dept_id)
            ).first()
            dept_name = dept.name if dept else "Desconhecido"
        
        department_stats.append(DepartmentStats(
            department_name=dept_name,
            response_count=len(dept_data),
            imco_average=round(sum(r['imco'] for r in dept_data) / len(dept_data), 2),
            fdac_average=round(sum(r['fdac'] for r in dept_data) / len(dept_data), 2)
        ))
    
    # Sort by response count descending
    department_stats.sort(key=lambda x: x.response_count, reverse=True)
    
    # Get recent responses (last 10)
    recent = db.query(Response).filter(
        Response.campaign_id == campaign_id,
        Response.completed_at.isnot(None)
    ).order_by(Response.completed_at.desc()).limit(10).all()
    
    recent_responses = []
    for r in recent:
        imco = calculate_imco_scores(r.answers, db)
        fdac = calculate_fdac_scores(r.answers, db)
        
        dept_name = None
        if r.department_id:
            dept = db.query(Department).filter(Department.id == r.department_id).first()
            dept_name = dept.name if dept else None
        
        recent_responses.append(ResponseDetail(
            id=str(r.id),
            department_name=dept_name,
            completed_at=r.completed_at.isoformat(),
            imco_overall=imco['overall'],
            fdac_overall=fdac['overall']
        ))
    
    # Completion rate (assuming all invited responded - simplified)
    completion_rate = 100.0  # For now, all submitted responses are complete
    
    return CampaignAnalytics(
        campaign_id=str(campaign.id),
        campaign_name=campaign.name,
        total_responses=total_responses,
        completion_rate=completion_rate,
        imco_overall=imco_overall,
        imco_vectors=imco_vectors_avg,
        imco_dimensions=imco_dimensions_avg,
        fdac_overall=fdac_overall,
        fdac_dimensions=fdac_dimensions_avg,
        department_stats=department_stats,
        recent_responses=recent_responses
    )


@router.get("/{campaign_id}/responses/{response_id}")
async def get_response_detail(
    campaign_id: uuid.UUID,
    response_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed breakdown of individual response"""
    response = db.query(Response).filter(
        Response.id == response_id,
        Response.campaign_id == campaign_id
    ).first()
    
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found"
        )
    
    # Calculate scores
    imco = calculate_imco_scores(response.answers, db)
    fdac = calculate_fdac_scores(response.answers, db)
    
    # Get department name
    dept_name = None
    if response.department_id:
        dept = db.query(Department).filter(Department.id == response.department_id).first()
        dept_name = dept.name if dept else None
    
    return {
        "id": str(response.id),
        "department_name": dept_name,
        "completed_at": response.completed_at.isoformat() if response.completed_at else None,
        "started_at": response.started_at.isoformat() if response.started_at else None,
        "imco": imco,
        "fdac": fdac,
        "answers": response.answers
    }

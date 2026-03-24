"""Demo routes - Handle demo request submissions"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime

from ..database import get_db
from ..models.demo_lead import DemoLead
from ..utils.time import get_current_time


router = APIRouter()


# Schemas
class DemoSubmit(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    empresa: str
    cargo: str | None = None
    mensagem: str | None = None


class DemoResponse(BaseModel):
    success: bool
    message: str
    lead_id: str


# Routes
@router.post("/submit", response_model=DemoResponse)
async def submit_demo_request(
    data: DemoSubmit,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Submit demo request from /demo page.
    Creates a lead for sales/marketing follow-up.
    """
    # Get client metadata
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # Create lead
    lead = DemoLead(
        nome=data.nome,
        email=data.email,
        telefone=data.telefone,
        empresa=data.empresa,
        cargo=data.cargo,
        mensagem=data.mensagem,
        ip_address=client_ip,
        user_agent=user_agent,
        created_at=get_current_time()
    )
    
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    return DemoResponse(
        success=True,
        message="Solicitação recebida com sucesso! Entraremos em contato em breve.",
        lead_id=str(lead.id)
    )


@router.get("/leads")
async def get_demo_leads(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all demo leads (admin only - add auth later).
    For now, returns all leads for admin panel.
    """
    leads = db.query(DemoLead).order_by(
        DemoLead.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "leads": [
            {
                "id": str(lead.id),
                "nome": lead.nome,
                "email": lead.email,
                "telefone": lead.telefone,
                "empresa": lead.empresa,
                "cargo": lead.cargo,
                "mensagem": lead.mensagem,
                "created_at": lead.created_at.isoformat()
            }
            for lead in leads
        ],
        "total": db.query(DemoLead).count()
    }

"""Demo Lead model - Contact form submissions"""
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..utils.time import get_current_time
import uuid

from ..database import Base


class DemoLead(Base):
    """
    Storage for demo request leads from /demo page.
    These are potential clients requesting demonstrations.
    """
    __tablename__ = "demo_leads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    telefone = Column(String(50), nullable=False)
    empresa = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=True)
    mensagem = Column(Text, nullable=True)
    
    # Tracking
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_current_time, nullable=False, index=True)
    
    def __repr__(self):
        return f"<DemoLead {self.email} - {self.empresa}>"

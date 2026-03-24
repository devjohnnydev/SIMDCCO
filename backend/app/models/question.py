"""Question model - IMCO and FDAC questions"""
from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from ..database import Base


class QuestionType(str, enum.Enum):
    """Type of questionnaire"""
    IMCO = "imco"  # 88 questions - organizational climate
    FDAC = "fdac"  # 12 questions - organizational culture


class Question(Base):
    """
    Questions for IMCO and FDAC questionnaires.
    Pre-populated with 100 validated questions.
    """
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SQLEnum(QuestionType), nullable=False, index=True)
    vector = Column(String(100), nullable=True)  # IMCO vectors
    dimension = Column(String(100), nullable=True)  # IMCO/FDAC dimensions
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)  # Display order (1-100)
    
    def __repr__(self):
        return f"<Question {self.id}: {self.type.value} - {self.text[:50]}>"

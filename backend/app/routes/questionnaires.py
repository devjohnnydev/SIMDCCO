"""Questionnaires routes - Get questions"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from ..database import get_db
from ..models.question import Question, QuestionType


router = APIRouter()


# Schemas
class QuestionResponse(BaseModel):
    id: int
    type: str
    vector: str | None
    dimension: str | None
    text: str
    order: int
    
    class Config:
        from_attributes = True


# Routes
@router.get("", response_model=List[QuestionResponse])
async def get_all_questions(db: Session = Depends(get_db)):
    """
    Get all 100 questions (88 IMCO + 12 FDAC) ordered by sequence.
    """
    questions = db.query(Question).order_by(Question.order).all()
    
    return [
        QuestionResponse(
            id=q.id,
            type=q.type.value,
            vector=q.vector,
            dimension=q.dimension,
            text=q.text,
            order=q.order
        )
        for q in questions
    ]


@router.get("/imco", response_model=List[QuestionResponse])
async def get_imco_questions(db: Session = Depends(get_db)):
    """Get only IMCO questions (88)"""
    questions = db.query(Question).filter(
        Question.type == QuestionType.IMCO
    ).order_by(Question.order).all()
    
    return [
        QuestionResponse(
            id=q.id,
            type=q.type.value,
            vector=q.vector,
            dimension=q.dimension,
            text=q.text,
            order=q.order
        )
        for q in questions
    ]


@router.get("/fdac", response_model=List[QuestionResponse])
async def get_fdac_questions(db: Session = Depends(get_db)):
    """Get only FDAC questions (12)"""
    questions = db.query(Question).filter(
        Question.type == QuestionType.FDAC
    ).order_by(Question.order).all()
    
    return [
        QuestionResponse(
            id=q.id,
            type=q.type.value,
            vector=q.vector,
            dimension=q.dimension,
            text=q.text,
            order=q.order
        )
        for q in questions
    ]

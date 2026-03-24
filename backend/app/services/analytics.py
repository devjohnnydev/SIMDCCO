"""Analytics service - Calculate IMCO and FDAC scores"""
from typing import Dict, List
from sqlalchemy.orm import Session
from ..models.response import Response
from ..models.question import Question, QuestionType
from ..models.analytic import Analytic, RiskLevel
from datetime import datetime, date
import uuid


def calculate_imco_scores(answers: Dict[str, int], db: Session) -> Dict:
    """
    Calculate IMCO scores from answers.
    
    Returns:
        {
            'vectors': {'Liderança': 4.2, ...},
            'dimensions': {'Apoio': 3.8, ...},
            'overall': 3.9
        }
    """
    # Get all IMCO questions
    questions = db.query(Question).filter(Question.type == QuestionType.IMCO).all()
    
    # Group by vector and dimension
    vector_scores = {}
    dimension_scores = {}
    all_scores = []
    
    for question in questions:
        q_id = str(question.id)
        if q_id in answers:
            score = answers[q_id]
            all_scores.append(score)
            
            # Group by vector
            if question.vector:
                if question.vector not in vector_scores:
                    vector_scores[question.vector] = []
                vector_scores[question.vector].append(score)
            
            # Group by dimension
            if question.dimension:
                if question.dimension not in dimension_scores:
                    dimension_scores[question.dimension] = []
                dimension_scores[question.dimension].append(score)
    
    # Calculate averages
    result = {
        'vectors': {v: round(sum(scores) / len(scores), 2) for v, scores in vector_scores.items()},
        'dimensions': {d: round(sum(scores) / len(scores), 2) for d, scores in dimension_scores.items()},
        'overall': round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    }
    
    return result


def calculate_fdac_scores(answers: Dict[str, int], db: Session) -> Dict:
    """
    Calculate FDAC scores from answers.
    
    Returns:
        {
            'dimensions': {'Poder': 3.5, ...},
            'overall': 3.6
        }
    """
    # Get all FDAC questions
    questions = db.query(Question).filter(Question.type == QuestionType.FDAC).all()
    
    # Group by dimension
    dimension_scores = {}
    all_scores = []
    
    for question in questions:
        q_id = str(question.id)
        if q_id in answers:
            score = answers[q_id]
            all_scores.append(score)
            
            if question.dimension:
                if question.dimension not in dimension_scores:
                    dimension_scores[question.dimension] = []
                dimension_scores[question.dimension].append(score)
    
    # Calculate averages
    result = {
        'dimensions': {d: round(sum(scores) / len(scores), 2) for d, scores in dimension_scores.items()},
        'overall': round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    }
    
    return result


def calculate_risk_level(overall_score: float) -> RiskLevel:
    """Determine risk level based on overall score"""
    if overall_score >= 4.0:
        return RiskLevel.LOW
    elif overall_score >= 3.0:
        return RiskLevel.MEDIUM
    elif overall_score >= 2.0:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


def calculate_organization_analytics(
    organization_id: uuid.UUID,
    department_id: uuid.UUID = None,
    db: Session = None
) -> Dict:
    """
    Calculate aggregated analytics for organization or department.
    
    Args:
        organization_id: Organization UUID
        department_id: Optional department UUID for filtered analysis
        db: Database session
    
    Returns:
        Dictionary with aggregated scores and statistics
    """
    # Query responses
    query = db.query(Response).filter(
        Response.organization_id == organization_id,
        Response.completed_at.isnot(None)
    )
    
    if department_id:
        query = query.filter(Response.department_id == department_id)
    
    responses = query.all()
    
    if not responses:
        return {
            'respondent_count': 0,
            'imco_scores': {},
            'fdac_scores': {},
            'risk_level': RiskLevel.LOW
        }
    
    # Aggregate all answers
    all_imco_vectors = {}
    all_imco_dimensions = {}
    all_fdac_dimensions = {}
    
    for response in responses:
        # Calculate individual scores
        imco = calculate_imco_scores(response.answers, db)
        fdac = calculate_fdac_scores(response.answers, db)
        
        # Aggregate IMCO
        for vector, score in imco['vectors'].items():
            if vector not in all_imco_vectors:
                all_imco_vectors[vector] = []
            all_imco_vectors[vector].append(score)
        
        for dimension, score in imco['dimensions'].items():
            if dimension not in all_imco_dimensions:
                all_imco_dimensions[dimension] = []
            all_imco_dimensions[dimension].append(score)
        
        # Aggregate FDAC
        for dimension, score in fdac['dimensions'].items():
            if dimension not in all_fdac_dimensions:
                all_fdac_dimensions[dimension] = []
            all_fdac_dimensions[dimension].append(score)
    
    # Calculate organization averages
    imco_scores = {
        'vectors': {v: round(sum(scores) / len(scores), 2) for v, scores in all_imco_vectors.items()},
        'dimensions': {d: round(sum(scores) / len(scores), 2) for d, scores in all_imco_dimensions.items()},
        'overall': round(
            sum(sum(scores) for scores in all_imco_vectors.values()) /
            sum(len(scores) for scores in all_imco_vectors.values()), 2
        ) if all_imco_vectors else 0
    }
    
    fdac_scores = {
        'dimensions': {d: round(sum(scores) / len(scores), 2) for d, scores in all_fdac_dimensions.items()},
        'overall': round(
            sum(sum(scores) for scores in all_fdac_dimensions.values()) /
            sum(len(scores) for scores in all_fdac_dimensions.values()), 2
        ) if all_fdac_dimensions else 0
    }
    
    # Calculate combined overall score for risk assessment
    combined_overall = round((imco_scores['overall'] + fdac_scores['overall']) / 2, 2)
    
    return {
        'respondent_count': len(responses),
        'imco_scores': imco_scores,
        'fdac_scores': fdac_scores,
        'risk_level': calculate_risk_level(combined_overall)
    }


def save_analytics(
    organization_id: uuid.UUID,
    department_id: uuid.UUID = None,
    period_start: date = None,
    period_end: date = None,
    db: Session = None
) -> Analytic:
    """
    Calculate and save analytics to database.
    
    Returns:
        Saved Analytic object
    """
    # Calculate analytics
    analytics_data = calculate_organization_analytics(organization_id, department_id, db)
    
    # Create analytic record
    analytic = Analytic(
        organization_id=organization_id,
        department_id=department_id,
        period_start=period_start or date.today(),
        period_end=period_end or date.today(),
        imco_scores=analytics_data['imco_scores'],
        fdac_scores=analytics_data['fdac_scores'],
        risk_level=analytics_data['risk_level'],
        respondent_count=analytics_data['respondent_count']
    )
    
    db.add(analytic)
    db.commit()
    db.refresh(analytic)
    
    return analytic

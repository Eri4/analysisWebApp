from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.database import get_db
from app.db.models import Analysis, Recommendation as RecommendationModel
from app.schemas.recommendation import Recommendation as RecommendationSchema
from app.services.llm_service import generate_recommendation

router = APIRouter()

@router.get("/", response_model=List[RecommendationSchema])
def get_recommendations(
        skip: int = 0,
        limit: int = 100,
        analysis_id: int = None,
        db: Session = Depends(get_db)
):
    """
    Get recommendations with optional filtering.
    """
    query = db.query(RecommendationModel)

    # Apply filters if provided
    if analysis_id:
        query = query.filter(RecommendationModel.analysis_id == analysis_id)

    # Apply pagination and return
    recommendations = query.order_by(RecommendationModel.created_at.desc()).offset(skip).limit(limit).all()
    return recommendations

@router.get("/{recommendation_id}", response_model=RecommendationSchema)
def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Get a specific recommendation by ID.
    """
    recommendation = db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()
    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation

@router.post("/generate/{analysis_id}", response_model=dict)
async def create_recommendation(
        analysis_id: int,
        db: Session = Depends(get_db)
):
    """
    Generate a new recommendation using LLM for a specific analysis.
    """
    # Check if analysis exists
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Since generate_recommendation is async, we can await it directly
    recommendation = await generate_recommendation(db, analysis)

    if recommendation:
        return {"message": "Recommendation generated successfully", "id": recommendation.id}
    else:
        return {"message": "Failed to generate recommendation"}
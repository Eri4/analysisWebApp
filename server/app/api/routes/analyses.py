from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.database import get_db
from app.db.models import Analysis as AnalysisModel, Recommendation
from app.schemas.analysis import Analysis as AnalysisSchema, AnalysisWithRecommendations
from app.services.analysis_service import run_analysis
from app.services.llm_service import generate_recommendation
from app.services.notification_service import send_notification_email

router = APIRouter()

@router.get("/", response_model=List[AnalysisSchema])
def get_analyses(
        skip: int = 0,
        limit: int = 100,
        type: str = None,
        metric: str = None,
        severity: str = None,
        db: Session = Depends(get_db)
):
    """
    Get analyses with optional filtering.
    """
    query = db.query(AnalysisModel)

    # Apply filters if provided
    if type:
        query = query.filter(AnalysisModel.type == type)
    if metric:
        query = query.filter(AnalysisModel.metric == metric)
    if severity:
        query = query.filter(AnalysisModel.severity == severity)

    # Apply pagination and return
    analyses = query.order_by(AnalysisModel.created_at.desc()).offset(skip).limit(limit).all()
    return analyses

@router.get("/{analysis_id}", response_model=AnalysisWithRecommendations)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get a specific analysis by ID including its recommendations.
    """
    analysis = db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.post("/run", response_model=Dict[str, str])
def trigger_analysis(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Trigger an immediate analysis of the campaign data.
    """
    background_tasks.add_task(run_analysis, db)
    return {"message": "Analysis started in background"}

@router.post("/{analysis_id}/notify", response_model=dict)
def send_notification(analysis_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Send a notification for a specific analysis.
    """
    analysis = db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    background_tasks.add_task(send_notification_email, db, analysis)
    return {"message": "Notification queued for sending"}
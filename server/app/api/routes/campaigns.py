from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.models import Campaign
from app.schemas.campaign import Campaign as CampaignSchema
from app.db.database import get_db

router = APIRouter()

@router.get("/", response_model=List[CampaignSchema])
def get_campaigns(
        skip: int = 0,
        limit: int = 100,
        campaign_name: Optional[str] = None,
        platform: Optional[str] = None,
        region: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        db: Session = Depends(get_db)
):
    """
    Get campaigns with optional filtering.
    """
    query = db.query(Campaign)

    # Apply filters if provided
    if campaign_name:
        query = query.filter(Campaign.campaign_name == campaign_name)
    if platform:
        query = query.filter(Campaign.platform == platform)
    if region:
        query = query.filter(Campaign.region == region)
    if start_date:
        query = query.filter(Campaign.date >= start_date)
    if end_date:
        query = query.filter(Campaign.date <= end_date)

    # Apply pagination and return
    campaigns = query.order_by(Campaign.date.desc()).offset(skip).limit(limit).all()
    return campaigns

@router.get("/{campaign_id}", response_model=CampaignSchema)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """
    Get a specific campaign by ID.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

from app.schemas.recommendation import RecommendationBase

class AnalysisBase(BaseModel):
    type: str
    metric: str
    description: str
    severity: str
    value: Optional[float] = None
    expected_value: Optional[float] = None
    date_range_start: Optional[date] = None
    date_range_end: Optional[date] = None

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: int
    created_at: datetime
    notified: bool

    class Config:
        from_attributes = True

class AnalysisWithRecommendations(Analysis):
    # Use a forward reference string instead of the actual class
    recommendations: List["RecommendationBase"] = []

    class Config:
        from_attributes = True
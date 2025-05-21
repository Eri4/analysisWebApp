from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecommendationBase(BaseModel):
    content: str

class RecommendationCreate(RecommendationBase):
    analysis_id: int

class Recommendation(RecommendationBase):
    id: int
    analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True
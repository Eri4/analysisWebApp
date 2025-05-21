from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class CampaignBase(BaseModel):
    campaign_name: str
    platform: str
    region: str
    date: date
    impressions: int
    clicks: int
    conversions: int
    spend: float

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    ctr: float
    cpc: float
    cpa: float
    created_at: datetime

    class Config:
        from_attributes = True

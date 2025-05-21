from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String(100), nullable=False)
    platform = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    conversions = Column(Integer, nullable=False)
    spend = Column(Float(precision=2), nullable=False)
    ctr = Column(Float(precision=4))  # Click-through rate
    cpc = Column(Float(precision=4))  # Cost per click
    cpa = Column(Float(precision=4))  # Cost per acquisition
    created_at = Column(DateTime(timezone=True), default=func.now())

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # 'anomaly', 'trend', 'summary'
    metric = Column(String(50), nullable=False)  # 'ctr', 'cpa', 'roi'
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # 'low', 'medium', 'high'
    value = Column(Float(precision=4))
    expected_value = Column(Float(precision=4))
    date_range_start = Column(Date)
    date_range_end = Column(Date)
    created_at = Column(DateTime(timezone=True), default=func.now())
    notified = Column(Boolean, default=False)

    # Relationships
    recommendations = relationship("Recommendation", back_populates="analysis")
    notifications = relationship("Notification", back_populates="analysis")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # Relationships
    analysis = relationship("Analysis", back_populates="recommendations")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    recipient = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=func.now())

    # Relationships
    analysis = relationship("Analysis", back_populates="notifications")
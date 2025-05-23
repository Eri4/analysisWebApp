from sqlalchemy.orm import Session
from sqlalchemy import func, and_, tuple_
from datetime import datetime, date, timedelta
import numpy as np
import logging

from app.core.config import settings
from app.services.llm_service import generate_recommendation
from app.services.notification_service import send_notification_email
from app.db.database import SessionLocal
from app.db.models import Campaign, Analysis

logger = logging.getLogger(__name__)


def run_analysis(db: Session):
    """Run analysis on campaign data to identify anomalies and trends."""
    logger.info("Starting campaign analysis...")

    # Get date range for analysis (last 10 days)
    end_date = db.query(func.max(Campaign.date)).scalar()
    if not end_date:
        logger.warning("No campaign data found")
        return

    start_date = end_date - timedelta(days=9)  # Analyze last 10 days

    # Run different types of analyses
    anomalies = detect_anomalies(db, start_date, end_date)

    # First, collect all the unique identifiers for our anomalies
    anomaly_identifiers = [
        (
            "anomaly",
            anomaly["metric"],
            anomaly["date"],
            anomaly["date"]
        )
        for anomaly in anomalies
    ]

    # Query existing anomalies in a single database call
    existing_anomalies = {}
    if anomaly_identifiers:
        existing_query = db.query(Analysis).filter(
            tuple_(
                Analysis.type,
                Analysis.metric,
                Analysis.date_range_start,
                Analysis.date_range_end
            ).in_(anomaly_identifiers)
        ).all()

        # Create a lookup dictionary
        for existing in existing_query:
            key = (
                existing.type,
                existing.metric,
                existing.date_range_start,
                existing.date_range_end
            )
            existing_anomalies[key] = existing

    # Collect new anomalies
    new_analyses = []
    for anomaly in anomalies:
        key = (
            "anomaly",
            anomaly["metric"],
            anomaly["date"],
            anomaly["date"]
        )

        # Skip if already exists
        if key in existing_anomalies:
            continue

        # Create new analysis record
        analysis = Analysis(
            type="anomaly",
            metric=anomaly["metric"],
            description=anomaly["description"],
            severity=anomaly["severity"],
            value=anomaly["value"],
            expected_value=anomaly["expected_value"],
            date_range_start=anomaly["date"],
            date_range_end=anomaly["date"]
        )
        new_analyses.append(analysis)

    # Bulk insert all new analyses
    if new_analyses:
        db.add_all(new_analyses)
        db.commit()

        # Process the newly added analyses
        for analysis in new_analyses:
            db.refresh(analysis)

            # Generate recommendation
            generate_recommendation(db, analysis)

            # Send notification for high severity
            if analysis.severity == "high":
                send_notification_email(db, analysis)

    logger.info("Analysis completed")


def detect_anomalies(db: Session, start_date: date, end_date: date):
    """Detect anomalies in campaign metrics."""
    anomalies = []

    # Get campaigns grouped by campaign identity
    campaigns = db.query(Campaign).filter(
        Campaign.date.between(start_date, end_date)
    ).order_by(Campaign.campaign_name, Campaign.platform, Campaign.region, Campaign.date).all()

    # Simple grouping
    current_group = []
    current_key = None

    for campaign in campaigns:
        key = (campaign.campaign_name, campaign.platform, campaign.region)

        # If we're starting a new group, process the previous one
        if current_key != key:
            if current_group:
                anomalies.extend(find_anomalies_in_group(current_group, current_key))
            current_group = [campaign]
            current_key = key
        else:
            current_group.append(campaign)

    # Process the last group
    if current_group:
        anomalies.extend(find_anomalies_in_group(current_group, current_key))

    return anomalies

def find_anomalies_in_group(campaigns, group_key):
    """Find anomalies within a single campaign group."""
    name, platform, region = group_key
    anomalies = []

    # Need at least 3 campaigns to detect anomalies
    if len(campaigns) < 3:
        return anomalies

    # Check each campaign against its historical average
    for i in range(2, len(campaigns)):  # Start from 3rd campaign
        current = campaigns[i]
        historical = campaigns[:i]  # All previous campaigns

        # Check each metric
        for metric_name in ['ctr', 'cpc', 'cpa']:
            current_value = getattr(current, metric_name)
            historical_values = [getattr(c, metric_name) for c in historical]

            # Simple anomaly check
            avg = sum(historical_values) / len(historical_values)

            # If current value is very different from average (more than 50% difference)
            if abs(current_value - avg) / avg > 0.5:  # 50% threshold
                direction = "increase" if current_value > avg else "decrease"
                percent_change = abs(current_value - avg) / avg * 100

                # Simple severity: >100% change = high, otherwise medium
                severity = "high" if percent_change > 100 else "medium"

                anomalies.append({
                    "metric": metric_name,
                    "description": f"Unusual {direction} in {metric_name.upper()} ({percent_change:.1f}%) for {name} on {platform} in {region}",
                    "severity": severity,
                    "value": float(current_value),
                    "expected_value": float(avg),
                    "date": current.date
                })

    return anomalies


def trigger_analysis():
    """Entry point to run analysis on demand."""
    db = SessionLocal()
    try:
        run_analysis(db)
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trigger_analysis()

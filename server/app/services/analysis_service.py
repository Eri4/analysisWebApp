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

    # Get all campaigns in date range
    campaigns = db.query(Campaign).filter(
        Campaign.date.between(start_date, end_date)
    ).all()

    # Group campaigns by name, platform, and region
    campaign_groups = {}
    for campaign in campaigns:
        key = (campaign.campaign_name, campaign.platform, campaign.region)
        if key not in campaign_groups:
            campaign_groups[key] = []
        campaign_groups[key].append(campaign)

    # Analyze each campaign group
    for (name, platform, region), group in campaign_groups.items():
        # Sort by date
        group.sort(key=lambda x: x.date)

        # Define metrics to analyze
        metrics = [
            {"name": "ctr", "getter": lambda c: c.ctr, "format": "percentage"},
            {"name": "cpc", "getter": lambda c: c.cpc, "format": "currency"},
            {"name": "cpa", "getter": lambda c: c.cpa, "format": "currency"}
        ]

        # Analyze each metric
        for metric in metrics:
            values = [metric["getter"](c) for c in group]
            mean = np.mean(values[:-1]) if len(values) > 1 else values[0]
            std = np.std(values[:-1]) if len(values) > 1 else 0

            for i, campaign in enumerate(group):
                # Skip the first day as we need historical data
                if i == 0:
                    continue

                # Check for anomaly
                if std > 0:
                    current_value = metric["getter"](campaign)
                    z_score = abs(current_value - mean) / std
                    if z_score > 2:  # More than 2 standard deviations
                        severity = "high" if z_score > 3 else "medium"

                        # Determine if it's a positive or negative anomaly
                        direction = "increase" if current_value > mean else "decrease"
                        percent_change = abs(current_value - mean) / mean * 100

                        format_suffix = "%" if metric["format"] == "percentage" else ""

                        anomalies.append({
                            "metric": metric["name"],
                            "description": f"Unusual {direction} in {metric['name'].upper()} ({percent_change:.1f}%) for {name} on {platform} in {region}",
                            "severity": severity,
                            "value": float(current_value),
                            "expected_value": float(mean),
                            "date": campaign.date
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

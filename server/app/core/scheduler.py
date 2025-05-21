from apscheduler.schedulers.background import BackgroundScheduler
from app.services.analysis_service import trigger_analysis
import logging

logger = logging.getLogger(__name__)

def setup_scheduler():
    """Setup and configure the APScheduler"""
    logger.info("Setting up scheduler")

    scheduler = BackgroundScheduler()

    # Add jobs to the scheduler
    # Run daily at midnight
    scheduler.add_job(
        trigger_analysis,
        'cron',
        hour=0,
        minute=0,
        id='daily_analysis',
        replace_existing=True,
        name='Daily Marketing Analysis'
    )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started")

    return scheduler
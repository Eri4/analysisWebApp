import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from sqlalchemy.orm import Session
from app.db.models import Analysis, Notification, Recommendation
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_notification_email(db: Session, analysis: Analysis):
    """Send email notification for an important analysis finding."""
    try:
        # Check if notification already sent
        if analysis.notified:
            logger.info(f"Notification already sent for analysis {analysis.id}")
            return

        # Get recommendations if any
        recommendations = db.query(Recommendation).filter(
            Recommendation.analysis_id == analysis.id
        ).all()

        # Create email subject and content
        subject = f"Marketing Alert: {analysis.severity.upper()} {analysis.type} in {analysis.metric}"

        # Create email content
        content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .severity-high {{ color: #dc3545; font-weight: bold; }}
                .severity-medium {{ color: #fd7e14; font-weight: bold; }}
                .severity-low {{ color: #20c997; font-weight: bold; }}
                .metric {{ font-weight: bold; }}
                .value {{ font-family: monospace; }}
                .recommendations {{ margin-top: 20px; }}
                .recommendation {{ margin-bottom: 15px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #007bff; }}
                .action-link {{ display: inline-block; margin-top: 15px; padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Marketing Campaign Alert</h2>
                    <p>We've detected a <span class="severity-{analysis.severity}">{analysis.severity}</span> {analysis.type} that requires your attention.</p>
                </div>
                
                <h3>Analysis Details</h3>
                <p><strong>Description:</strong> {analysis.description}</p>
                <p><strong>Metric:</strong> <span class="metric">{analysis.metric}</span></p>
                <p><strong>Current Value:</strong> <span class="value">{analysis.value:.4f}</span></p>
                <p><strong>Expected Value:</strong> <span class="value">{analysis.expected_value:.4f}</span></p>
                <p><strong>Date Range:</strong> {analysis.date_range_start} to {analysis.date_range_end}</p>
                
                <div class="recommendations">
                    <h3>Recommendations</h3>
        """

        if recommendations:
            for recommendation in recommendations:
                content += f"""
                    <div class="recommendation">
                        <p>{recommendation.content}</p>
                    </div>
                """
        else:
            content += """
                    <p>Recommendations are being generated and will be available on the dashboard.</p>
            """

        # Add link to dashboard
        content += f"""
                </div>
                
                <a href="http://localhost:3000/analysis/{analysis.id}" class="action-link">View Details in Dashboard</a>
            </div>
        </body>
        </html>
        """

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = settings.EMAILS_FROM_EMAIL
        msg["To"] = settings.EMAILS_TO_EMAIL
        msg["Subject"] = subject

        # Attach HTML content
        msg.attach(MIMEText(content, "html"))

        # Send email
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        # Mark as notified
        analysis.notified = True

        # Add notification record
        notification = Notification(
            analysis_id=analysis.id,
            recipient=settings.EMAILS_TO_EMAIL,
            subject=subject,
            content=content
        )

        db.add(notification)
        db.commit()

        logger.info(f"Notification sent for analysis {analysis.id}")
        return True

    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False
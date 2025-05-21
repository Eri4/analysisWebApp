import httpx
import json
import logging
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import Analysis, Recommendation, Campaign
from app.core.config import settings

logger = logging.getLogger(__name__)

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Simple in-memory rate limiter
last_api_call = datetime.min
min_call_interval = timedelta(seconds=2)  # Wait at least 2 seconds between calls

async def generate_recommendation(db: Session, analysis: Analysis):
    """Generate recommendation for an analysis using Mistral API."""
    global last_api_call

    try:
        # Rate limiting
        now = datetime.now()
        time_since_last_call = now - last_api_call
        if time_since_last_call < min_call_interval:
            sleep_time = (min_call_interval - time_since_last_call).total_seconds()
            logger.info(f"Rate limiting: Waiting {sleep_time:.2f} seconds before API call")
            await asyncio.sleep(sleep_time)

        # Get campaign data related to the analysis
        campaigns = db.query(Campaign).filter(
            Campaign.date.between(analysis.date_range_start, analysis.date_range_end)
        ).all()

        # Prepare campaign data summary for context
        campaign_summary = []
        for campaign in campaigns:
            campaign_summary.append({
                "name": campaign.campaign_name,
                "platform": campaign.platform,
                "region": campaign.region,
                "date": str(campaign.date),
                "impressions": campaign.impressions,
                "clicks": campaign.clicks,
                "conversions": campaign.conversions,
                "spend": campaign.spend,
                "ctr": campaign.ctr,
                "cpc": campaign.cpc,
                "cpa": campaign.cpa
            })

        # Create prompt for the LLM
        prompt = f"""
        You are a marketing analytics expert. Based on the following analysis and campaign data, provide actionable recommendations.
        
        ANALYSIS:
        Type: {analysis.type}
        Metric: {analysis.metric}
        Description: {analysis.description}
        Severity: {analysis.severity}
        Current Value: {analysis.value}
        Expected Value: {analysis.expected_value}
        Date Range: {analysis.date_range_start} to {analysis.date_range_end}
        
        CAMPAIGN DATA:
        {json.dumps(campaign_summary, indent=2)}
        
        Provide 3 specific, actionable recommendations to address this issue. Each recommendation should:
        1. Be specific to the platform, campaign, and region involved
        2. Suggest a concrete action to take
        3. Explain the expected outcome of taking this action
        
        Format your response as 3 separate recommendations without numbering or bullet points.
        """

        # Call Mistral API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}"
        }

        payload = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                MISTRAL_API_URL,
                headers=headers,
                json=payload
            )

            # Update last API call timestamp after making the request
            last_api_call = datetime.now()

            if response.status_code == 200:
                response_data = response.json()
                recommendation_text = response_data["choices"][0]["message"]["content"]

                # Save recommendation to database
                recommendation = Recommendation(
                    analysis_id=analysis.id,
                    content=recommendation_text
                )
                db.add(recommendation)
                db.commit()
                db.refresh(recommendation)

                return recommendation
            else:
                logger.error(f"Error from Mistral API: {response.text}")
                return None

    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return None
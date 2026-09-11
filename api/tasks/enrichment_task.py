from api.tasks.celery_app import celery_app
import asyncio
from api.database import AsyncSessionLocal
from api.models.lead import Lead, LeadStatusEnum
from sqlalchemy.future import select
from datetime import datetime
from api.services.enrichment_orchestrator import orchestrate_enrichment

@celery_app.task(name="enrich_lead")
def run_enrichment(lead_id: str):
    asyncio.run(_async_run_enrichment(lead_id))

async def _async_run_enrichment(lead_id: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Lead).filter(Lead.id == str(lead_id)))
        lead = result.scalars().first()
        
        if not lead:
            return
            
        lead.status = LeadStatusEnum.processing
        await db.commit()
        
        try:
            enrichment_result = await orchestrate_enrichment(str(lead.id), lead.original_data)
            
            lead.enriched_data = enrichment_result.get("enriched_data")
            lead.score_value = enrichment_result.get("score_value")
            lead.score_grade = enrichment_result.get("score_grade")
            lead.score_breakdown = enrichment_result.get("score_breakdown")
            lead.score_recommendation = enrichment_result.get("score_recommendation")
            lead.status = LeadStatusEnum.completed
            lead.enriched_at = datetime.utcnow()
            
        except Exception:
            lead.status = LeadStatusEnum.failed
        finally:
            await db.commit()

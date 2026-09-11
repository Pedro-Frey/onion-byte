from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from api.models.lead import Lead, LeadStatusEnum
from api.schemas.lead import LeadEnrichRequest

async def create_lead(db: AsyncSession, lead_data: LeadEnrichRequest, user_id: str) -> Lead:
    db_lead = Lead(
        user_id=user_id,
        original_data=lead_data.model_dump(),
        status=LeadStatusEnum.pending
    )
    db.add(db_lead)
    await db.commit()
    await db.refresh(db_lead)
    return db_lead

async def get_lead_by_id(db: AsyncSession, lead_id: str, user_id: str) -> Lead:
    result = await db.execute(select(Lead).filter(Lead.id == str(lead_id), Lead.user_id == str(user_id)))
    return result.scalars().first()

async def list_leads(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Lead).filter(Lead.user_id == str(user_id)).offset(skip).limit(limit))
    return result.scalars().all()

async def get_leads(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 10):
    items_query = select(Lead).filter(Lead.user_id == str(user_id)).offset(skip).limit(limit)
    items_result = await db.execute(items_query)
    
    count_query = select(func.count()).select_from(Lead).filter(Lead.user_id == str(user_id))
    count_result = await db.execute(count_query)
    
    return items_result.scalars().all(), count_result.scalar()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from api.models.usage import UsageLog

async def log_usage(db: AsyncSession, user_id: str, endpoint: str, response_time_ms: int, status_code: int):
    log = UsageLog(
        user_id=user_id,
        endpoint=endpoint,
        response_time_ms=response_time_ms,
        status_code=status_code,
        credits_used=1
    )
    db.add(log)
    await db.commit()

async def get_user_usage_summary(db: AsyncSession, user_id: str):
    logs_result = await db.execute(select(UsageLog).filter(UsageLog.user_id == str(user_id)).order_by(UsageLog.request_at.desc()).limit(100))
    logs = logs_result.scalars().all()
    
    total_requests_query = select(func.count()).select_from(UsageLog).filter(UsageLog.user_id == str(user_id))
    total_requests = (await db.execute(total_requests_query)).scalar()
    
    total_credits_query = select(func.sum(UsageLog.credits_used)).filter(UsageLog.user_id == str(user_id))
    total_credits = (await db.execute(total_credits_query)).scalar() or 0
    
    return {
        "total_requests": total_requests,
        "total_credits_used": total_credits,
        "logs": logs
    }

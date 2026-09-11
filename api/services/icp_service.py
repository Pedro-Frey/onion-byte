from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models.icp import ICP
from api.schemas.icp import ICPCreate

async def get_icp(db: AsyncSession, user_id: str) -> ICP:
    result = await db.execute(select(ICP).filter(ICP.user_id == str(user_id)))
    return result.scalars().first()

async def create_or_update_icp(db: AsyncSession, icp_data: ICPCreate, user_id: str) -> ICP:
    icp = await get_icp(db, user_id)
    if not icp:
        icp = ICP(user_id=user_id, **icp_data.model_dump())
        db.add(icp)
    else:
        for key, value in icp_data.model_dump().items():
            setattr(icp, key, value)
    
    await db.commit()
    await db.refresh(icp)
    return icp

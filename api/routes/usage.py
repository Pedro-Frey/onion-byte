from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api.schemas.usage import UsageSummary
from api.middleware.auth import get_current_user
from api.models.user import User
from api.services.usage_service import get_user_usage_summary

router = APIRouter()

@router.get("/", response_model=UsageSummary)
async def get_usage(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna o resumo de uso e créditos da API do usuário."""
    return await get_user_usage_summary(db, current_user.id)

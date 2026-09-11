from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api.schemas.icp import ICPCreate, ICPResponse
from api.middleware.auth import get_current_user
from api.models.user import User
from api.services.icp_service import create_or_update_icp, get_icp

router = APIRouter()

@router.post("/configure", response_model=ICPResponse)
async def configure_icp(icp_data: ICPCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Configura ou atualiza o Perfil de Cliente Ideal (ICP) do usuário."""
    return await create_or_update_icp(db, icp_data, str(current_user.id))

@router.get("/", response_model=ICPResponse)
async def get_user_icp(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna o Perfil de Cliente Ideal (ICP) configurado pelo usuário."""
    icp = await get_icp(db, str(current_user.id))
    if not icp:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="ICP não configurado")
    return icp

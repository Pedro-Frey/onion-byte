from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from api.services.auth_service import get_user_by_email, create_user, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registra um novo usuário no sistema."""
    user = await get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    new_user = await create_user(db, user_data)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Autentica o usuário e retorna o token JWT."""
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

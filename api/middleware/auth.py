"""
Middleware de autenticação JWT e API Key.
"""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.config import settings
from api.database import get_db
from api.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def create_access_token(data: dict) -> str:
    """Cria um token de acesso JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decodifica e valida um token JWT."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    db: AsyncSession = Depends(get_db)
) -> User:
    """DEV MODE: Retorna usuário de teste e salva no banco se não existir."""
    result = await db.execute(select(User))
    user = result.scalars().first()
    if not user:
        import uuid
        import bcrypt
        new_id = uuid.uuid4()
        hashed = bcrypt.hashpw(b"test1234", bcrypt.gensalt()).decode("utf-8")
        user = User(
            id=new_id, 
            email="teste@onionbyte.com", 
            hashed_password=hashed, 
            company_name="Modo de Teste",
            api_key="test-key"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

async def get_current_user_by_api_key(
    api_key: str = Security(api_key_header),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Extrai e retorna o usuário logado a partir da API Key."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key não fornecida",
        )
    
    result = await db.execute(select(User).where(User.api_key == api_key))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida",
        )
    return user

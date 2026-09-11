from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets
from api.config import settings
from api.models.user import User
from api.schemas.auth import UserRegister

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(select(User).filter(User.id == str(user_id)))
    return result.scalars().first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def generate_api_key():
    return secrets.token_urlsafe(32)

async def create_user(db: AsyncSession, user: UserRegister) -> User:
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        company_name=user.company_name,
        api_key=generate_api_key()
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

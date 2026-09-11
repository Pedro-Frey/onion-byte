from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    company_name: Optional[str]
    plan: str
    api_key: Optional[str]
    
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

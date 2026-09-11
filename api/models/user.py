import uuid
from sqlalchemy import Column, String, DateTime, Integer, Enum, Uuid
from sqlalchemy.sql import func
from api.database import Base
import enum

class PlanEnum(str, enum.Enum):
    free = "free"
    starter = "starter"
    pro = "pro"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    company_name = Column(String)
    api_key = Column(String, unique=True, index=True)
    plan = Column(Enum(PlanEnum), default=PlanEnum.free)
    request_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

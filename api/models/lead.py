import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from api.database import Base
import enum

class LeadStatusEnum(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"))
    original_data = Column(JSONB)
    enriched_data = Column(JSONB)
    score_value = Column(Float)
    score_grade = Column(String)
    score_breakdown = Column(JSONB)
    score_recommendation = Column(Text)
    status = Column(Enum(LeadStatusEnum), default=LeadStatusEnum.pending)
    enriched_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

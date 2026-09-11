import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Uuid
from sqlalchemy.sql import func
from api.database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"))
    endpoint = Column(String)
    request_at = Column(DateTime(timezone=True), server_default=func.now())
    response_time_ms = Column(Integer)
    status_code = Column(Integer)
    credits_used = Column(Integer, default=1)

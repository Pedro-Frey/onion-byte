import uuid
from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, String, Uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from api.database import Base

class ICP(Base):
    __tablename__ = "icps"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id"))
    industry = Column(ARRAY(String))
    company_size = Column(ARRAY(String))
    job_titles = Column(ARRAY(String))
    location = Column(ARRAY(String))
    revenue_min = Column(BigInteger)
    revenue_max = Column(BigInteger)
    custom_criteria = Column(ARRAY(String))
    deal_breakers = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ICPBase(BaseModel):
    industry: Optional[List[str]] = []
    company_size: Optional[List[str]] = []
    job_titles: Optional[List[str]] = []
    location: Optional[List[str]] = []
    revenue_min: Optional[int] = None
    revenue_max: Optional[int] = None
    custom_criteria: Optional[List[str]] = []
    deal_breakers: Optional[List[str]] = []

class ICPCreate(ICPBase):
    pass

class ICPUpdate(ICPBase):
    pass

class ICPResponse(ICPBase):
    id: UUID
    user_id: UUID
    
    model_config = {"from_attributes": True}

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class UsageResponse(BaseModel):
    id: UUID
    endpoint: str
    request_at: datetime
    response_time_ms: int
    status_code: int
    credits_used: int
    
    model_config = {"from_attributes": True}

class UsageSummary(BaseModel):
    total_requests: int
    total_credits_used: int
    logs: List[UsageResponse]

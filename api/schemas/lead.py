from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID

class LeadEnrichRequest(BaseModel):
    name: str
    email: str
    phone: str
    cpf: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class LeadEnrichResponse(BaseModel):
    id: UUID
    status: str
    original_data: Dict[str, Any]
    enriched_data: Optional[Dict[str, Any]] = None
    score_value: Optional[float] = None
    score_grade: Optional[str] = None
    score_breakdown: Optional[Dict[str, Any]] = None
    score_recommendation: Optional[str] = None
    
    model_config = {"from_attributes": True}

class LeadListResponse(BaseModel):
    items: List[LeadEnrichResponse]
    total: int
    page: int
    size: int

class LeadBatchRequest(BaseModel):
    leads: List[LeadEnrichRequest]

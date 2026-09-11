from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api.schemas.lead import LeadEnrichRequest, LeadEnrichResponse, LeadListResponse, LeadBatchRequest
from api.middleware.auth import get_current_user
from api.models.user import User
from api.services.lead_service import create_lead, get_lead_by_id, get_leads
from api.tasks.enrichment_task import run_enrichment

router = APIRouter()

@router.post("/enrich", response_model=LeadEnrichResponse)
async def enrich_lead(lead_data: LeadEnrichRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Envia um lead para enriquecimento. Inicia a tarefa assíncrona."""
    lead = await create_lead(db, lead_data, current_user.id)
    run_enrichment.delay(str(lead.id))
    return lead

@router.get("/{id}", response_model=LeadEnrichResponse)
async def get_lead(id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna o status e dados de um lead específico."""
    lead = await get_lead_by_id(db, id, current_user.id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead

@router.get("/", response_model=LeadListResponse)
async def list_leads(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Lista todos os leads do usuário com paginação."""
    leads, total = await get_leads(db, current_user.id, skip, limit)
    return {"items": leads, "total": total, "page": skip // limit + 1, "size": limit}

@router.post("/batch")
async def enrich_leads_batch(batch_data: LeadBatchRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Envia múltiplos leads para enriquecimento."""
    leads = []
    for lead_data in batch_data.leads:
        lead = await create_lead(db, lead_data, current_user.id)
        run_enrichment.delay(str(lead.id))
        leads.append(lead)
    return {"message": f"{len(leads)} leads enviados para processamento."}

@router.get("/{id}/score", response_model=LeadEnrichResponse)
async def get_lead_score(id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna apenas o score de um lead (atalho para get_lead)."""
    lead = await get_lead_by_id(db, id, current_user.id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead

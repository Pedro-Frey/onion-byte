from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    """Verificação de integridade da API."""
    return {"status": "ok"}

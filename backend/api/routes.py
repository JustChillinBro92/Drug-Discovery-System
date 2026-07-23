from fastapi import APIRouter
from api.response_models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )
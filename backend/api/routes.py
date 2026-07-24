from fastapi import APIRouter

from api.request_models import DrugQueryRequest
from api.response_models import HealthResponse

from pipeline.pipeline import execute

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )
    
@router.post("/analyze")
def analyze_drug(request: DrugQueryRequest):
    result = execute(request.query)
    
    return result
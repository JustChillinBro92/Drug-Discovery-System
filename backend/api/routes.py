from fastapi import APIRouter

from api.request_models import AnalysisRequest
from api.response_models import (
    HealthCheckResponse,
    AnalysisResponse
)

from backend.pipeline.run_pipeline import execute

router = APIRouter()


@router.get("/health", response_model= HealthCheckResponse)
def health_check():
    return  HealthCheckResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )
    
    
@router.post("/analyze", response_model=AnalysisResponse)
def analyze(
    request: AnalysisRequest
):
    result = execute(
        conversation_id=request.conversation_id,
        mode=request.mode,
        query=request.query
    )

    return AnalysisResponse(
        conversation_id=request.conversation_id,
        mode=request.mode,
        result=result
    )
from fastapi import APIRouter

from api.request_models import (
    AnalysisRequest,
    ConversationRequest
)
from api.response_models import (
    HealthCheckResponse,
    AnalysisResponse,
    ConversationResponse
)
from models.conversation_state import ConversationState

from backend.pipeline.run_pipeline import execute
from backend.pipeline.run_free_conversation import execute as execute_conversation

router = APIRouter()


@router.get("/health", response_model= HealthCheckResponse)
def health_check():
    return  HealthCheckResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )
    
    
@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    result = execute(
        mode=request.mode,
        query=request.query,
        state=ConversationState()
    )

    return AnalysisResponse(
        mode=request.mode,
        result=result
    )


@router.post(
    "/chat/{conversation_id}",
    response_model=ConversationResponse
)
def free_conversation(
    conversation_id: str,
    request: ConversationRequest
):
    result = execute_conversation(
        conversation_id=conversation_id,
        query=request.query
    )

    return ConversationResponse(
        conversation_id=conversation_id,
        mode="free_conversation",
        result=result
    )
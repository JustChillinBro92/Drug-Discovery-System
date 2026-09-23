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

from pipeline.run_pipeline import execute
from pipeline.run_free_conversation import run_user_input

router = APIRouter()


@router.get("/health", response_model= HealthCheckResponse)
def health_check():
    return  HealthCheckResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )
    
    
@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    arguments = {}
    
    if request.mode == "literature_acquisition":
        arguments["page_size"] = request.page_size
    elif request.mode == "similar_compound_search":
        arguments["target_compounds"] = request.target_compounds
    
    result = execute(
        mode=request.mode,
        query=request.query,
        state=ConversationState(),
        **arguments
    )

    return AnalysisResponse(
        mode=request.mode,
        result=result
    )


@router.post("/c/{conversation_id}", response_model=ConversationResponse)
def free_conversation(
    conversation_id: str,
    request: ConversationRequest
):
    return run_user_input(
        conversation_id=conversation_id,
        query=request.query
    )
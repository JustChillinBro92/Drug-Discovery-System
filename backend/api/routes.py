from fastapi import APIRouter, HTTPException, Response

from api.request_models import (
    AnalysisRequest,
    ConversationRequest
)
from api.response_models import (
    HealthCheckResponse,
    AnalysisResponse,
    ConversationResponse
)

from pipeline.run_pipeline import execute
from pipeline.run_free_conversation import (
    clear_session,
    create_session,
    get_or_create_session,
    run_user_input
)

from services.sources.chembl_service import chembl_service

router = APIRouter()


@router.get("/health", response_model= HealthCheckResponse)
def health_check():
    return HealthCheckResponse(
        status="healthy",
        service="Drug Discovery RAG"
    )


@router.post("/sessions")
def create_conversation():
    conversation_id, _ = create_session()
    return {"conversation_id": conversation_id}


@router.post("/c/{conversation_id}/clear")
def clear_conversation(conversation_id: str):
    try:
        clear_session(conversation_id)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    return {
        "conversation_id": conversation_id,
        "message": "Conversation cleared"
    }
    
    
@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    arguments = {}
    
    if request.mode == "literature_acquisition":
        arguments["page_size"] = request.page_size
    elif request.mode == "similar_compound_search":
        arguments["target_compounds"] = request.target_compounds
    
    if request.conversation_id is not None:
        conversation_id, session = get_or_create_session(
            str(request.conversation_id)
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="conversation_id is required"
        )

    result = execute(
        mode=request.mode,
        query=request.query,
        state=session["state"],
        **arguments
    )

    return AnalysisResponse(
        conversation_id=conversation_id,
        mode=request.mode,
        result=result
    )


@router.get("/image/{chembl_id}")
def get_compound_image(chembl_id: str):
    try:
        image_content = chembl_service.get_molecule_image(
            chembl_id
        )
        
        return Response(
            content=image_content,
            media_type="image/svg+xml"
        )
        
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve compound image: {error}"
        ) from error


@router.post("/c/{conversation_id}", response_model=ConversationResponse)
def free_conversation(
    conversation_id: str,
    request: ConversationRequest
):
    return run_user_input(
        conversation_id=conversation_id,
        query=request.query
    )
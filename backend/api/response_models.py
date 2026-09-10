from typing import Any, Literal

from pydantic import BaseModel

from models.pipeline_response import PipelineResponse


class HealthCheckResponse(BaseModel):
    status: str
    service: str


class AnalysisResponse(BaseModel):
    mode: str
    result: Any


class ConversationResponse(BaseModel):
    conversation_id: str
    mode: Literal["free_conversation"]
    result: PipelineResponse
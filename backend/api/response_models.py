from typing import Any, Literal

from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    status: str
    service: str


class AnalysisResponse(BaseModel):
    mode: str
    result: Any


class ConversationResponse(BaseModel):
    conversation_id: str
    mode: Literal["free_conversation"]
    message: str
    data: dict[str, Any]
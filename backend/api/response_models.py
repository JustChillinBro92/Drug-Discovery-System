from typing import Any

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    service: str


class AnalysisResponse(BaseModel):
    conversation_id: str
    mode: str
    result: Any
from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    conversation_id: str
    mode: str
    query: str
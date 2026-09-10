from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    mode: str
    query: str


class ConversationRequest(BaseModel):
    query: str
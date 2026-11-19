from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    conversation_id: str | None = None
    mode: str
    query: str
    page_size: int | None = None
    target_compounds: list[str] | None = None


class ConversationRequest(BaseModel):
    query: str
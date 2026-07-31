from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class EntityState(BaseModel):
    compounds: List[str] = Field(default_factory=list)
    diseases: List[str] = Field(default_factory=list)
    proteins: List[str] = Field(default_factory=list)


class ConversationState(BaseModel):
    conversation_id: str

    current_mode: Optional[str] = None

    entities: EntityState = Field(
        default_factory=EntityState
    )

    paper_ids: List[str] = Field(
        default_factory=list
    )

    important_context: List[str] = Field(
        default_factory=list
    )
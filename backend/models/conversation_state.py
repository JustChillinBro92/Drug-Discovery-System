from typing import List, Optional

from pydantic import BaseModel, Field

from models.paper_entity import PaperEntity



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

    indexed_papers: List[PaperEntity] = Field(
        default_factory=list,
        description="Research papers indexed into the local vector store for this conversation."
    )
    
    retrieved_chunk_ids: List[str] = Field(
        default_factory=list,
        description="Chunk IDs retrieved during previous literature conversations."
    )

    important_context: List[str] = Field(
        default_factory=list,
        description="Conversation-specific facts that should persist across mode switches."
    )
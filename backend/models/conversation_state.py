from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from models.similarity_search_result import SimilarCompound
from models.referenced_paper import ReferencedPaper
from models.compound_analysis import CompoundAnalysis


class EntitySummary(BaseModel):
    protein_count: int = 0
    side_effect_count: int = 0
    treatable_disease_count: int = 0


class EntityState(BaseModel):
    compound_details: CompoundAnalysis
    summary: EntitySummary = Field(default_factory=EntitySummary)
    
    def update_compound(self, compound: CompoundAnalysis):
        self.compound_details = compound

    def update_proteins(self, proteins: List):
        self.summary.protein_count = len(proteins)

    def update_side_effects(self, side_effects: List):
        self.summary.side_effect_count = len(side_effects)

    def update_treatable_diseases(self, diseases: List):
        self.summary.treatable_disease_count = len(diseases)


class LiteratureRetrievalState(BaseModel):
    query: str

    category: Optional[str] = None

    retrieved_chunk_ids: List[str] = Field(
        default_factory=list,
        description="Chunk IDs retrieved for this literature retrieval."
    )

    referenced_papers: List[ReferencedPaper] = Field(
        default_factory=list,
        description="Papers referenced during this literature retrieval."
    )

    offset: int = 0


class ConversationState(BaseModel):
    conversation_id: str

    current_mode: Optional[str] = None

    analyzed_compounds: List[EntityState] = Field(
        default_factory=list,
        description="Compounds and summary data analyzed during this conversation."
    )
    
    similarity_results: List[SimilarCompound] = Field(
        default_factory=list,
        description="Similarity comparisons performed during this conversation."
    )

    # referenced_papers: List[ReferencedPaper] = Field(
    #     default_factory=list,
    #     description="Papers used in this conversation."
    # )
    
    # retrieved_chunk_ids: List[str] = Field(
    #     default_factory=list,
    #     description="Chunk IDs retrieved during previous literature conversations."
    # )
    
    referenced_paper_ids: set[str] = Field(
        default_factory=set
    )

    literature_retrievals: Dict[
        str,
        LiteratureRetrievalState
    ] = Field(
        default_factory=dict
    )

    important_context: List[str] = Field(
        default_factory=list,
        description="Conversation-specific facts that should persist across mode switches."
    )
from typing import List, Optional

from pydantic import BaseModel, Field

from models.similarity_search_result import SimilarCompound
from models.referenced_paper import ReferencedPaper
from models.compound_analysis import CompoundAnalysis


class EntityState(BaseModel):
    compounds: List[str] = Field(default_factory=list)
    diseases: List[str] = Field(default_factory=list)
    proteins: List[str] = Field(default_factory=list)
    
    def add_compound(self, compound: str):
        if compound not in self.compounds:
            self.compounds.append(compound)
            
    def add_disease(self, disease: str):
        if disease not in self.diseases:
            self.diseases.append(disease)

    def add_protein(self, protein: str):
        if protein not in self.proteins:
            self.proteins.append(protein)



class ConversationState(BaseModel):
    conversation_id: str

    current_mode: Optional[str] = None

    entities: EntityState = Field(
        default_factory=EntityState
    )
    
    analyzed_compounds: List[CompoundAnalysis] = Field(
        default_factory=list,
        description="Compounds analyzed during this conversation."
    )
    
    similarity_results: List[SimilarCompound] = Field(
        default_factory=list,
        description="Similarity comparisons performed during this conversation."
    )

    referenced_papers: List[ReferencedPaper] = Field(
        default_factory=list,
        description="Papers used in this conversation."
    )
    
    retrieved_chunk_ids: List[str] = Field(
        default_factory=list,
        description="Chunk IDs retrieved during previous literature conversations."
    )

    important_context: List[str] = Field(
        default_factory=list,
        description="Conversation-specific facts that should persist across mode switches."
    )
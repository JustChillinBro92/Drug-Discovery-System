from pydantic import BaseModel, Field


"""
Represents one chunk of text extracted from a research paper.
"""

class DocumentChunk(BaseModel):
    chunk_id: str = Field(
        ...,
        description="Unique identifier for the chunk."
    )
    
    paper_pmid: str = Field(
        ...,
        description="PubMed ID of the source paper."
    )
    
    chunk_index: int = Field(
        ...,
        ge=0,
        description="Position of this chunk within the paper."
    )
    
    text: str = Field(
        ...,
        min_length=1,
        description="Text content of the paper."
    )
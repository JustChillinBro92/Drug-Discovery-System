from pydantic import BaseModel, Field

class SimilarityResult(BaseModel):
    compound_name: str = Field(
        ...,
        description="Name of compared compound."
    )
    
    similarity_score: float = Field(
        ...,
        ge = 0.0,
        le = 1.0,
        description="Tanimoto similarity score."
    )
    
    
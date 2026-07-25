from pydantic import BaseModel, Field


class SimilarCompound(BaseModel):
    compound_name: str = Field(
        ...,
        description="Name of similar compound."
    )
    
    chembl_id: str = Field(
        ...,
        description="ChEMBL id."
    )
    
    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Tanimoto similarity score."
    )
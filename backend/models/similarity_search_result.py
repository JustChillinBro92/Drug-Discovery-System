from pydantic import BaseModel, Field


class SimilarCompound(BaseModel):
    query_compound: str = Field(
        ...,
        description="Compound used as the similarity search query."
    )

    compound_name: str = Field(
        ...,
        description="Name of the compound compared against the query compound."
    )

    chembl_id: str = Field(
        ...,
        description="ChEMBL ID of the compared compound."
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Tanimoto similarity score between the query and compared compounds."
    )
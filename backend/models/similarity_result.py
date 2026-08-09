from pydantic import BaseModel, Field


class SimilarityResult(BaseModel):
    query_compound: str = Field(
        ...,
        description="Compound used as the similarity search query."
    )

    compared_compound: str = Field(
        ...,
        description="Compound compared against the query compound."
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Tanimoto similarity score between the two compounds."
    )
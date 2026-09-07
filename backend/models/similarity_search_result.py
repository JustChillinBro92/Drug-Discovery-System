from pydantic import BaseModel, Field


class SimilarCompound(BaseModel):
    query_original_text: str = Field(
        ...,
        description="Original query compound text entered by the user."
    )

    query_compound: str = Field(
        ...,
        description="Compound used as the similarity search query."
    )

    compound_original_text: str = Field(
        ...,
        description="Original compared compound text entered by the user."
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
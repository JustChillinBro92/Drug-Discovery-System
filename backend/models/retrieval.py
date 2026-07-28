from pydantic import BaseModel, Field

from models.document_chunk import DocumentChunk


class RetrievalResult(BaseModel):
    """
    Represents a document chunk retrieved from the vector store.
    """

    chunk: DocumentChunk = Field(
        ...,
        description="The retrieved document chunk."
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Cosine similarity score between the query and the retrieved chunk."
    )
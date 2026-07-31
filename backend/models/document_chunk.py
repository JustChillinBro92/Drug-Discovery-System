from typing import Optional

from pydantic import BaseModel, Field


"""
Represents one chunk of text extracted from a research paper.
"""


class DocumentChunk(BaseModel):

    chunk_id: str = Field(
        ...,
        description="Unique identifier for the chunk."
    )

    pmid: Optional[str] = Field(
        default=None,
        description="PubMed identifier of the source paper."
    )

    pmcid: Optional[str] = Field(
        default=None,
        description="PubMed Central identifier of the source paper."
    )

    doi: Optional[str] = Field(
        default=None,
        description="Digital Object Identifier of the source paper."
    )

    title: Optional[str] = Field(
        default=None,
        description="Title of the source paper."
    )

    journal: Optional[str] = Field(
        default=None,
        description="Journal in which the paper was published."
    )

    publication_year: Optional[int] = Field(
        default=None,
        ge=1800,
        description="Publication year of the source paper."
    )

    authors: list[str] = Field(
        default_factory=list,
        description="Authors of the source paper."
    )

    chunk_index: int = Field(
        ...,
        ge=0,
        description="Position of this chunk within the paper."
    )

    text: str = Field(
        ...,
        min_length=1,
        description="Text content of the chunk."
    )
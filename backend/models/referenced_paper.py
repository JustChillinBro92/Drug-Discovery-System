from typing import Optional

from pydantic import BaseModel, Field


class ReferencedPaper(BaseModel):
    """
    Represents a research paper that was used
    during a conversation.
    """

    pmid: Optional[str] = Field(
        default=None,
        description="PubMed identifier of the referenced paper."
    )

    pmcid: Optional[str] = Field(
        default=None,
        description="PubMed Central identifier of the referenced paper."
    )

    doi: Optional[str] = Field(
        default=None,
        description="DOI of the referenced paper."
    )

    title: str = Field(
        ...,
        description="Title of the referenced paper."
    )

    journal: Optional[str] = Field(
        default=None,
        description="Journal where the paper was published."
    )

    publication_year: Optional[int] = Field(
        default=None,
        description="Publication year of the paper."
    )

    url: Optional[str] = Field(
        default=None,
        description="URL to the paper."
    )

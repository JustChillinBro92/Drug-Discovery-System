from typing import Optional
from pydantic import BaseModel, Field


"""
Represents a biomedical research paper retrieved from Europe PMC.
"""

class PaperEntity(BaseModel):
    pmid: Optional[str] = Field(
        default=None,
        description="PubMed identifier for the research paper."
    )

    pmcid: Optional[str] = Field(
        default=None,
        description="PubMed Central identifier for the full-text article, if available."
    )

    doi: Optional[str] = Field(
        default=None,
        description="Digital Object Identifier (DOI) of the publication."
    )

    title: str = Field(
        ...,
        description="Title of the research paper."
    )

    abstract: Optional[str] = Field(
        default=None,
        description="Abstract summarizing the research paper."
    )

    authors: list[str] = Field(
        default_factory=list,
        description="List of authors who contributed to the publication."
    )

    journal: Optional[str] = Field(
        default=None,
        description="Name of the journal in which the paper was published."
    )

    publication_year: Optional[int] = Field(
        default=None,
        ge=1800,
        description="Year in which the paper was published."
    )

    publication_date: Optional[str] = Field(
        default=None,
        description="Complete publication date in ISO format when available."
    )

    publication_types: list[str] = Field(
        default_factory=list,
        description="Type of publication (e.g., Journal Article, Clinical Trial, Review)."
    )
    
    keywords: list[str] = Field(
        default_factory=list,
        description="Author-provided keywords associated with the paper."
    )
    
    mesh_terms: list[str] = Field(
        default_factory=list,
        description="Medical Subject Headings (MeSH) terms associated with the paper."
    )

    source: str = Field(
        default="Europe PMC",
        description="Source database from which the paper was retrieved."
    )

    open_access: bool = Field(
        default=False,
        description="Indicates whether the full-text paper is available as open access."
    )

    in_pmc: bool = Field(
        default=False,
        description="Indicates whether the paper is available in PubMed Central."
    )

    cited_by_count: int = Field(
        default=0,
        ge=0,
        description="Number of times the paper has been cited according to Europe PMC."
    )

    url: Optional[str] = Field(
        default=None,
        description="Direct URL to the paper or its Europe PMC record."
    )
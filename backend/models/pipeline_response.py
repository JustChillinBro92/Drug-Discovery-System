from typing import Any, Optional

from pydantic import BaseModel


class SourceReference(BaseModel):
    title: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None
    doi: Optional[str] = None
    journal: Optional[str] = None
    publication_year: Optional[int] = None
    url: Optional[str] = None
    

class PipelineResponse(BaseModel):
    mode: str
    answer: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    message: Optional[str] = None
    papers_added: Optional[int] = None
    chunks_added: Optional[int] = None
    sources: list[SourceReference] = []
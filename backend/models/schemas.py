from typing import List, Optional
from pydantic import BaseModel


class NormalizedEntity(BaseModel):
    original_text: str
    canonical_name: str
    entity_type: str
    database: str
    database_id: str
    confidence: float
    metadata: dict = {}
    
    
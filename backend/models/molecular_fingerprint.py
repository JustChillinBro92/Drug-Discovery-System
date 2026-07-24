from typing import List, Optional
from pydantic import BaseModel, Field


"""
Represents a molecular fingerprint generated using RDKit.

Used for:
- compound similarity search
- nearest neighbor retrieval
- analog identification
"""

class MolecularFingerprint(BaseModel):
    fingerprint_type: str = Field(
        ...,
        description="Fingerprint algorithm used (Morgan)."
    )

    radius: Optional[int] = Field(
        default=None,
        description="Radius used for circular fingerprints like Morgan."
    )

    bit_length: int = Field(
        ...,
        gt=0,
        description="Number of bits in fingerprint vector."
    )

    bit_vector: List[int] = Field(
        ...,
        description="Binary fingerprint representation."
    )
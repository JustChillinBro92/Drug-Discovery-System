from typing import List
from pydantic import BaseModel, Field


class MolecularFingerprint(BaseModel):
    algorithm: str = Field(
        ...,
        description="Fingerprint algorithm used."
    )

    radius: int = Field(
        ...,
        description="Morgan fingerprint radius."
    )

    n_bits: int = Field(
        ...,
        description="Fingerprint size."
    )

    fingerprint: List[int] = Field(
        ...,
        description="Binary fingerprint vector."
    )
from typing import Optional

from pydantic import BaseModel, Field

# Lipinski Rule of Five evaluation

class LipinskiResult(BaseModel):
    molecular_weight_pass: bool
    logp_pass: bool
    hbd_pass: bool
    hba_pass: bool
    overall_pass: bool
    violations: int = Field(
        ...,
        ge=0,
        description="Number of Lipinski rule violations."
    )


# Molecular descriptors calculated using RDKit 

class MolecularProperties(BaseModel):
    molecular_weight: float = Field(
        ...,
        description="Molecular weight (Daltons)."
    )

    logp: float = Field(
        ...,
        description="Octanol/water partition coefficient."
    )

    tpsa: float = Field(
        ...,
        description="Topological Polar Surface Area."
    )

    h_bond_donors: int = Field(
        ...,
        ge=0,
        description="Number of hydrogen bond donors."
    )

    h_bond_acceptors: int = Field(
        ...,
        ge=0,
        description="Number of hydrogen bond acceptors."
    )

    rotatable_bonds: int = Field(
        ...,
        ge=0,
        description="Number of rotatable bonds."
    )

    heavy_atoms: int = Field(
        ...,
        ge=0,
        description="Number of heavy atoms."
    )

    ring_count: int = Field(
        ...,
        ge=0,
        description="Number of rings."
    )

    aromatic_ring_count: int = Field(
        ...,
        ge=0,
        description="Number of aromatic rings."
    )

    formal_charge: int = Field(
        ...,
        description="Formal molecular charge."
    )

    fraction_csp3: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Fraction of sp3 hybridized carbons."
    )

    qed: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Quantitative Estimate of Drug-likeness."
    )

    lipinski: LipinskiResult
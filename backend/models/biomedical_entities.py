from typing import List, Optional
from pydantic import BaseModel, Field


# Base Biomedical Entity
# Base class for all normalized entities

class BaseBioMedicalEntity(BaseModel):
    original_text: str = Field(
        ...,
        description="Entity exactly as extracted from the user's query."
    )

    canonical_name: str = Field(
        ...,
        description="Canonical name returned by the source database."
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalization confidence score."
    )

    synonyms: List[str] = Field(
        default_factory=list,
        description="Known synonyms of the entity."
    )
    
    
    
    
# Different Normalized Entity Type classes
# Inherits from parent class BaseBioMedicalEntity

# Compound Entity class (ChemBL)

class CompoundEntity(BaseBioMedicalEntity):
    chembl_id: str
    smiles: str
    inchikey: str
    molecular_formula: Optional[str] = None
    
    
# Protein Entity class (UniProt)

class ProteinEntity(BaseBioMedicalEntity):
    uniprot_id: str
    gene_symbol: Optional[str] = None
    protein_name: Optional[str] = None
    organism: Optional[str] = None
    
    
# Disease Entity class (DisGeNET)

class DiseaseEntity(BaseBioMedicalEntity):
    disease_id: str
    ontology: Optional[str] = None
    mesh_id: Optional[str] = None
    
    
# Side Effect Entity class (SIDER)

class SideEffectEntity(BaseBioMedicalEntity):
    sider_id: Optional[str] = None
    frequency: Optional[str] = None
    severity: Optional[str] = None
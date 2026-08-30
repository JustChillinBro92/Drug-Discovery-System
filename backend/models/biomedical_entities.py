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

    # synonyms: List[str] = Field(
    #     default_factory=list,
    #     description="Known synonyms of the entity."
    # )
    
    
    
    
# Different Normalized Entity Type classes
# Inherits from parent class BaseBioMedicalEntity


# Compound Entity class (ChemBL)

class CompoundEntity(BaseBioMedicalEntity):
    chembl_id: str = Field(
        ...,
        description="ChEMBL identifier for the compound."
    )

    smiles: str = Field(
        ...,
        description="Canonical SMILES representation of the compound."
    )

    inchikey: str = Field(
        ...,
        description="InChIKey identifier of the compound."
    )

    molecular_formula: Optional[str] = Field(
        default=None,
        description="Molecular formula of the compound."
    )
    
    
    
# Protein Entity class (UniProt)

class ProteinEntity(BaseModel):
    uniprot_id: str = Field(
        ...,
        description="UniProt accession for the protein."
    )

    protein_name: Optional[str] = Field(
        default=None,
        description="Recommended name of the protein."
    )

    gene_symbol: Optional[str] = Field(
        default=None,
        description="Primary gene symbol associated with the protein."
    )

    organism: Optional[str] = Field(
        default=None,
        description="Organism in which the protein is found."
    )

    function: Optional[str] = Field(
        default=None,
        description="Biological function of the protein."
    )

    subcellular_location: Optional[str] = Field(
        default=None,
        description="Subcellular location of the protein."
    )
    
    pathways: list[str] = Field(
        default_factory=list,
        description="Biological pathways associated with the protein."
    )
    
    sequence: Optional[str] = Field(
        default=None,
        description="Amino acid sequence of the protein."
    )

    sequence_length: Optional[int] = Field(
        default=None,
        description="Length of the protein sequence in amino acids."
    )
    
    
    
# Disease Entity class (DisGeNET)

class DiseaseEntity(BaseBioMedicalEntity):
    disease_id: str = Field(
        ...,
        description="DisGeNET identifier for the disease."
    )

    ontology: Optional[str] = Field(
        default=None,
        description="Disease ontology associated with the disease."
    )

    mesh_id: Optional[str] = Field(
        default=None,
        description="MeSH identifier associated with the disease."
    )
    
    
    
# Side Effect Entity class (SIDER)

class SideEffectEntity(BaseBioMedicalEntity):
    sider_id: Optional[str] = Field(
        default=None,
        description="SIDER identifier for the side effect."
    )

    frequency: Optional[str] = Field(
        default=None,
        description="Reported frequency of the side effect."
    )

    severity: Optional[str] = Field(
        default=None,
        description="Reported severity of the side effect."
    )
    
    
    
# Pathway Entity class (KEGG)

class PathwayEntity(BaseBioMedicalEntity):
    kegg_id: str = Field(
        ...,
        description="KEGG identifier for the biological pathway."
    )

    pathway_name: Optional[str] = Field(
        default=None,
        description="Name of the biological pathway."
    )

    organism: Optional[str] = Field(
        default=None,
        description="Organism associated with the pathway."
    )
    
    

# Docking Result Entity class

class DockingResultEntity(BaseModel):
    """
    Represents a computational molecular docking result.

    Unlike normalized biomedical entities, a docking result
    represents an experimental/computational relationship
    between a compound and a protein.
    """

    docking_id: str = Field(
        ...,
        description="Unique identifier for the docking result."
    )

    compound_id: str = Field(
        ...,
        description="Identifier of the compound evaluated in docking."
    )

    protein_id: str = Field(
        ...,
        description="Identifier of the protein used as the docking target."
    )

    binding_affinity: Optional[float] = Field(
        default=None,
        description="Predicted binding affinity from the docking result."
    )

    docking_score: Optional[float] = Field(
        default=None,
        description="Docking score produced by the docking software."
    )

    binding_mode: Optional[str] = Field(
        default=None,
        description="Predicted binding mode of the compound."
    )

    software: Optional[str] = Field(
        default=None,
        description="Docking software used to generate the result."
    )

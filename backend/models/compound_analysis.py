from pydantic import BaseModel

from models.biomedical_entities import CompoundEntity
from models.molecular_properties import MolecularProperties


class CompoundAnalysis(BaseModel):
    compound: CompoundEntity
    properties: MolecularProperties
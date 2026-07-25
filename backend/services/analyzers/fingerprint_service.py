from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

from models.biomedical_entities import CompoundEntity
from models.molecular_fingerprint import MolecularFingerprint


"""
Generate Morgan fingerprint for a compound.
-------------------------------------------
Default:
radius = 2
bits = 2048
"""

class FingerprintService:
    def generate_morgan_fingerprint(
        self,
        compound: CompoundEntity,
        radius: int = 2,
        n_bits: int = 2048
    ) -> MolecularFingerprint:

        # 1. Verify compound SMILES first
        
        molecule = Chem.MolFromSmiles(compound.smiles)
        
        if molecule is None:
            raise ValueError(
                f"Invalid SMILES for compound {compound.canonical_name}!"
            )
               
        # 2. Get the fingerprint bit vector
        
        generator = rdFingerprintGenerator.GetMorganGenerator(
            radius=int(radius),
            fpSize=int(n_bits)
        )
        
        fingerprint = generator.GetFingerprint(
            molecule
        )
        
        # 3. Convert the explicit bit vector into a python List
        
        fingerprint_bits = [int(bit) for bit in fingerprint]
        
        
        return MolecularFingerprint(
            algorithm="Morgan",
            radius = radius,
            n_bits = n_bits,
            fingerprint = fingerprint_bits
        )
        
fingerprint_service = FingerprintService()
        
        
        
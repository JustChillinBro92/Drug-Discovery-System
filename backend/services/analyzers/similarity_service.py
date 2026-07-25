from rdkit import DataStructs
from rdkit.DataStructs.cDataStructs import ExplicitBitVect

from models.similarity_result import SimilarityResult
from models.molecular_fingerprint import MolecularFingerprint


"""
Calculate Tanimoto similarity between two fingerprints.
"""

class SimilarityService:
    def convert_to_bitvector(
        self,
        fingerprint: MolecularFingerprint
    ):
        
        bit_vector = ExplicitBitVect(
            fingerprint.n_bits
        )
        
        for index, bit in enumerate(
            fingerprint.fingerprint
        ):
            if bit == 1:
                bit_vector.SetBit(index)
                
        return bit_vector
    
    
    def calculate_similarity(
        self,
        query_fingerprint: MolecularFingerprint,
        target_fingerprint: MolecularFingerprint,
        target_name: str
    ) -> SimilarityResult:
        
        # Back convert fingerprint python list to bit vector
        
        query_fp = self.convert_to_bitvector(
            query_fingerprint
        )
        
        target_fp = self.convert_to_bitvector(
            target_fingerprint
        )        
        
        
        # Calculate the Tanimoto similarity btwn both fingerprints
        
        score = DataStructs.TanimotoSimilarity(
            query_fp, target_fp
        )
        
        return SimilarityResult(
            compound_name = target_name,
            similarity_score = score
        )
        
similarity_service = SimilarityService()
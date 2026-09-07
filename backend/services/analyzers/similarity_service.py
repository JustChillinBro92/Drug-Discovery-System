from rdkit import DataStructs
from rdkit.DataStructs.cDataStructs import ExplicitBitVect

from models.similarity_result import SimilarityResult
from models.similarity_search_result import SimilarCompound
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
        query_original_text: str,
        query_name: str,
        target_original_text: str,
        target_name: str,
        target_chembl_id: str
    ) -> SimilarityResult:

        # Convert fingerprints back to RDKit bit vectors

        query_fp = self.convert_to_bitvector(
            query_fingerprint
        )

        target_fp = self.convert_to_bitvector(
            target_fingerprint
        )


        # Calculate Tanimoto similarity

        score = DataStructs.TanimotoSimilarity(
            query_fp,
            target_fp
        )

        return SimilarCompound(
            query_original_text=query_original_text,
            query_compound=query_name,
            compound_original_text=target_original_text,
            compound_name=target_name,
            chembl_id=target_chembl_id,
            similarity_score=score
        )


similarity_service = SimilarityService()
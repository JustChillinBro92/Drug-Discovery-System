from models.molecular_fingerprint import MolecularFingerprint
from models.similarity_search_result import SimilarCompound

from services.analyzers.similarity_service import similarity_service


class SimilaritySearchService:
    def search_similar_compounds(
        self,
        query_fingerprint: MolecularFingerprint,
        query_name: str,
        query_chembl_id: str,
        query_original_text: str,
        compounds: list[dict]
    ) -> list[SimilarCompound]:

        """
        Loops through all target compounds, calculates
        Tanimoto similarity against the query compound,
        and returns all results sorted by similarity.
        """

        results = []

        for item in compounds:

            similarity_result = (
                similarity_service.calculate_similarity(
                    query_fingerprint,
                    item["fingerprint"],
                    query_original_text,
                    query_name,
                    query_chembl_id,
                    item["original_text"],
                    item["compound"].canonical_name,
                    item["compound"].chembl_id
                )
            )

            results.append(similarity_result)

        results.sort(
            key=lambda x: x.similarity_score,
            reverse=True
        )

        return results


similarity_search_service = SimilaritySearchService()
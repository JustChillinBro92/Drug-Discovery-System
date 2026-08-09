from models.molecular_fingerprint import MolecularFingerprint
from models.similarity_search_result import SimilarCompound

from services.analyzers.similarity_service import similarity_service


class SimilaritySearchService:

    def search_similar_compounds(
        self,
        query_fingerprint: MolecularFingerprint,
        query_name: str,
        compounds: list[dict],
        top_k: int = 5
    ) -> list[SimilarCompound]:

        """
        Loops through all target compounds, calculates
        Tanimoto similarity against the query compound,
        and returns the top-k results.
        """

        results = []

        for item in compounds:

            similarity_result = (
                similarity_service.calculate_similarity(
                    query_fingerprint,
                    item["fingerprint"],
                    query_name,
                    item["compound"].canonical_name,
                    item["compound"].chembl_id
                )
            )

            results.append(similarity_result)

        results.sort(
            key=lambda x: x.similarity_score,
            reverse=True
        )

        return results[:top_k]


similarity_search_service = SimilaritySearchService()
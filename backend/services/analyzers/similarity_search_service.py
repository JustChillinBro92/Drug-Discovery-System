from models.molecular_fingerprint import MolecularFingerprint
from models.similarity_search_result import SimilarCompound

from services.analyzers.similarity_service import similarity_service



class SimilaritySearchService:
    def search_similar_compounds(
        self,
        query_fingerprint: MolecularFingerprint,
        compounds: list[dict],
        top_k: int = 5
    ) -> SimilarCompound:
        
        """ 
        Loops through all the compounds, calculates similarity score,
        appends pair (compound, score) to result & filters out top-k pairs
        according to score
                       
        """
        
        results = []
        
        for item in compounds:
            
            score = similarity_service.calculate_similarity(
                query_fingerprint,
                item["fingerprint"],
                item["compound"].canonical_name
            )
            
            results.append(
                SimilarCompound(
                    compound_name = item["compound"].canonical_name,
                    chembl_id = item["compound"].chembl_id,
                    similarity_score = score.similarity_score
                )
            )
            
        results.sort(
            key = lambda x: x.similarity_score,
            reverse = True
        )
        
        return results[:top_k]
    
similarity_search_service = SimilaritySearchService()
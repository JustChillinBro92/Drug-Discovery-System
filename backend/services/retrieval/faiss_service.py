import faiss
import numpy as np

from models.document_chunk import DocumentChunk
from models.retrieval import RetrievalResult


class FAISS_Service:
    """
    Initializes an empty FAISS index (Vector DB).

    Since our embeddings are L2-normalized, IndexFlatIP
    performs cosine similarity search.
    """
    
    def __init__(
        self,
        dimension: int = 384
    ):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Maintains mapping:
        # FAISS index i <-> self.chunks[i]
        self.chunks: list[DocumentChunk] = []
        
    
    """ 
    Adds document chunks and their embeddings to FAISS 
    """
    
    def add_documents(
        self,
        chunks: list[DocumentChunk],
        embeddings: np.ndarray
    ) -> None:
        
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings didn't match!"
            )
            
        self.index.add(embeddings)
        self.chunks.extend(chunks)
        
    
    """ 
    Searches for the most similar document chunks
    according to user query 
    """
    
    def search_documents(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> list[RetrievalResult]:
        
        # Reshape the query embedding to 2d numpy array from 1d numpy array
        # reshape(row, column) -> -1 auto decides columns required
        # [[0.95, 0.91, 0.83]] -> 1 row, 3 columns => shape = (1, 3)
        
        query_embedding = query_embedding.reshape(1, -1)
        
        
        # Find the top_k similarity scores & their corresponding FAISS indices
        
        scores, indices = self.index.search(
            query_embedding,
            top_k
        )
        
        
        # Populate the result array with pairs of chunk and it's score
        
        results = []
        
        for score, indx in zip(
            scores[0],
            indices[0]
        ):
            if indx == -1:
                continue
            
            results.append(
                RetrievalResult(
                    chunk=self.chunks[indx],
                    similarity_score=float(score)
                )
            )
        
        return results
        

faiss_service = FAISS_Service()        
        
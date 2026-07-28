import numpy as np
from sentence_transformers import SentenceTransformer

from models.document_chunk import DocumentChunk


class EmbeddingService:
    """ Loads the embedding model once when the service starts """
    
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    """
    Generate an embedding for a single text (user query)
    Returns: NumPy array of shape (384,)
    """

    def embed_text(
        self,
        text: str
    ) -> np.ndarray:
        
        embedding = self.model.encode(
            text,
            normalize_embeddings = True,
            convert_to_numpy = True
        )
        
        return embedding.astype(np.float32)
    
    
    """
    Generate embeddings for multiple document chunks
    Returns: NumPy array of shape (N, 384)
    """
    
    def embed_chunks(
        self,
        chunks: list[DocumentChunk]
    ) -> np.ndarray:
        
        texts = [
            chunk.text
            for chunk in chunks
        ]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings = True,
            convert_to_numpy = True
        )
        
        return embeddings.astype(np.float32)
    
    
embedding_service = EmbeddingService()
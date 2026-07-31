from rag.embedding_service import embedding_service
from rag.faiss_service import faiss_service


"""
Retrieves relevant chunks for a user query
"""

class Retriever:
    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):
        # Convert user query to embeddings
        
        query_embeddings = embedding_service.embed_text(
            query                        
        )
        
        # Search vector database
        
        results = faiss_service.search_documents(
            query_embeddings,
            top_k
        )
        
        return results
    
    
retriever = Retriever()
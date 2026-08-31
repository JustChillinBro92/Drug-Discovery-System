from rag.embedding_service import embedding_service
from rag.vector_store import vector_store


"""
Retrieves relevant chunks for a user query
"""

class Retriever:
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        offset: int = 0
    ):
        # Convert user query to embeddings
        
        query_embeddings = embedding_service.embed_text(
            query                        
        )
        
        # Search vector database
        
        results = vector_store.search_documents(
            query_embeddings,
            top_k,
            offset
        )
        
        return results
    
    
retriever = Retriever()
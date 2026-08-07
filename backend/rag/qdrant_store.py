import numpy as np
from typing import List
from pathlib import Path

import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from models.paper_entity import PaperEntity
from models.document_chunk import DocumentChunk
from models.retrieval import RetrievalResult


BASE_DIR = Path(__file__).resolve().parents[2]
QDRANT_PATH = BASE_DIR / "data" / "qdrant"


class QdrantStore:
    def __init__(
        self,
        collection_name: str = "biomedical_documents"
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(
            path=str(QDRANT_PATH)
        )
        self._create_collection()
        
        
    def _create_collection(self):
        collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]
        
        if self.collection_name not in collections:
            
            self.client.create_collection(
                collection_name=self.collection_name,  
                  
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )


    """
    Adds document chunks and embeddings to Qdrant
    """

    def add_documents(
        self,
        chunks: List[DocumentChunk],
        embeddings: np.ndarray
    ) -> None:
        
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings didn't match!"
            )
        
        points = []
        
        for index, chunk in enumerate(chunks):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embeddings[index].tolist(),
                    payload={
                        "chunk_id": chunk.chunk_id,

                        "pmid": chunk.pmid,
                        "pmcid": chunk.pmcid,
                        "doi": chunk.doi,

                        "title": chunk.title,
                        "journal": chunk.journal,
                        "publication_year": chunk.publication_year,

                        "authors": chunk.authors,

                        "url": chunk.url,

                        "chunk_index": chunk.chunk_index,

                        "text": chunk.text                        
                    }
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        
    """
    Searches for most similar document chunks
    """        
           
    def search_documents(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> list[RetrievalResult]:
        
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            with_payload=True
        )
        
        retrieved_results = []
        
        for point in results.points:
            payload = point.payload
            
            chunk = DocumentChunk(**payload)
            
            retrieved_results.append(
                RetrievalResult(
                    chunk=chunk,
                    similarity_score=float(point.score)
                )
            )
            
        return retrieved_results
    
    
    """
    View papers indexed into Qdrant payload
    """
     
    def get_indexed_papers(self):
        
        papers = {}
        
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000
        )
        
        for point in points:
            payload = point.payload
            
            paper_id = (
                payload.get("pmid") or
                payload.get("pmcid") or
                payload.get("doi")
            )
            
            if not paper_id:
                continue
            
            if paper_id not in papers:
                papers[paper_id] = {
                    "pmid": payload.get("pmid"),
                    "pmcid": payload.get("pmcid"),
                    "doi": payload.get("doi"),
                    "title": payload.get("title"),
                    "authors": payload.get("authors", []),
                    "journal": payload.get("journal"),
                    "publication_year": payload.get("publication_year"),
                    "url": payload.get("url"),
                    "texts": []
                }
                
            papers[paper_id]["texts"].append(
                payload.get("text", "")
            )
            
        results = []
        
        for paper in papers.values():
            
            results.append(
                PaperEntity(
                    pmid=paper["pmid"],
                    pmcid=paper["pmcid"],
                    doi=paper["doi"],
                    title=paper["title"],
                    abstract="\n\n".join(
                        paper["texts"]
                    ),
                    authors=paper["authors"],
                    journal=paper["journal"],
                    publication_year=paper["publication_year"],
                    url=paper["url"]
                )
            )                
                
            
        return results
        
    
    """
    Check if a paper already indexed into Qdrant
    """
    
    def paper_exists(
        self,
        paper_id: str
    ) -> bool:

        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                should=[
                    FieldCondition(
                        key="pmid",
                        match=MatchValue(
                            value=paper_id
                        )
                    ),
                    FieldCondition(
                        key="pmcid",
                        match=MatchValue(
                            value=paper_id
                        )
                    ),
                    FieldCondition(
                        key="doi",
                        match=MatchValue(
                            value=paper_id
                        )
                    )
                ]
            ),

            limit=1
        )


        return len(points) > 0
   
    
    
    def clear_collection(self):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[]
            )
        )

        # pending
        # self._initialize_collection()
        

qdrant_store = QdrantStore()
    
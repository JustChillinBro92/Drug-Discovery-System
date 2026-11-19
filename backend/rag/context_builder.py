from models.referenced_paper import ReferencedPaper
from models.retrieval import RetrievalResult
from models.pipeline_response import SourceReference

class ContextBuilder:
    def build_context(
        self,
        results: list[RetrievalResult],
    ):
        
        context_parts = []
        sources = []
        referenced_papers = []

        seen_sources = set()
        source_map = {}
        
        for index, result in enumerate(
            results,
            start = 1
        ):
            
            chunk = result.chunk
            similarity_score = result.similarity_score
            
            paper_id = (
                chunk.pmid
                or chunk.pmcid
                or chunk.doi
                or "Unknown"
            )
             
            context_parts.append(
                f"""
                    Source {index}                   
                    PMID: {chunk.pmid or "Unknown"}
                    PMCID: {chunk.pmcid or "Unknown"}
                    DOI: {chunk.doi or "Unknown"}              
                    Text: {chunk.text or "Unknown"}
                """
            )
            
            
            # Avoid duplicate paper citations
            
            if paper_id not in seen_sources:
                source = SourceReference(
                    title=chunk.title or "Unknown",
                    chunk_ids=[chunk.chunk_id],
                    pmid=chunk.pmid,
                    pmcid=chunk.pmcid,
                    doi=chunk.doi,
                    journal=chunk.journal,
                    publication_year=chunk.publication_year,
                    url=chunk.url,
                    similarity_score=similarity_score
                )
                
                sources.append(source)
                source_map[paper_id] = source
                
                referenced_papers.append(
                    ReferencedPaper(
                        pmid=chunk.pmid,
                        pmcid=chunk.pmcid,
                        doi=chunk.doi,
                        title=chunk.title or "Unknown",
                        authors=chunk.authors,
                        keywords=chunk.keywords,
                        journal=chunk.journal,
                        publication_year=chunk.publication_year,
                        url=chunk.url
                    )                    
                )
                
                seen_sources.add(paper_id)
            else:
                source_map[paper_id].chunk_ids.append(chunk.chunk_id)
            
        return (
            "\n\n".join(context_parts), 
            sources, 
            referenced_papers
        )
        

context_builder = ContextBuilder()

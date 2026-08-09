from models.paper_entity import PaperEntity
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
        

        for index, result in enumerate(
            results,
            start = 1
        ):
            
            chunk = result.chunk
            
            paper_id = (
                chunk.pmid
                or chunk.pmcid
                or chunk.doi
                or "Unknown"
            )
             
            context_parts.append(
                f"""
                    Source {index}
                    
                    PMID:
                    {chunk.pmid or "Unknown"}

                    PMCID:
                    {chunk.pmcid or "Unknown"}

                    DOI:
                    {chunk.doi or "Unknown"}
                    
                    Text:
                    {chunk.text or "Unknown"}
                """
            )
            
            
            # Avoid duplicate paper citations
            
            if paper_id not in seen_sources:
                sources.append(
                    SourceReference(
                        title=chunk.title or "Unknown",
                        chunk_id=chunk.chunk_id,
                        pmid=chunk.pmid,
                        pmcid=chunk.pmcid,
                        doi=chunk.doi,
                        journal=chunk.journal,
                        publication_year=chunk.publication_year,
                        url=chunk.url
                    )
                )
                
                referenced_papers.append(
                    ReferencedPaper(
                        pmid=chunk.pmid,
                        pmcid=chunk.pmcid,
                        doi=chunk.doi,
                        title=chunk.title or "Unknown",
                        authors=chunk.authors,
                        journal=chunk.journal,
                        publication_year=chunk.publication_year,
                        url=chunk.url
                    )                    
                )
                
                seen_sources.add(paper_id)
            
        return ("\n\n".join(context_parts), sources, referenced_papers)
        

context_builder = ContextBuilder()

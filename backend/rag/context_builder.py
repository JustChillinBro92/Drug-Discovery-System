from models.paper_entity import PaperEntity
from models.retrieval import RetrievalResult
from models.pipeline_response import SourceReference

class ContextBuilder:
    def build_context(
        self,
        results: list[RetrievalResult]
    ):
        
        context_parts = []
        sources = []
        # referenced_papers = []
        
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
                        title = chunk.title or "Unknown",
                        chunk_id = chunk.chunk_id,
                        pmid = chunk.pmid or "Unknown",
                        pmcid = chunk.pmcid or "Unknown",
                        doi = chunk.doi or "Unknown",
                        journal = chunk.journal or "Unknown",
                        publication_year = chunk.publication_year or "Unknown",
                        url = chunk.url or "Unknown"
                    )
                )
                
                # referenced_papers.append(
                #     PaperEntity(
                #         pmid=chunk.pmid,
                #         pmcid=chunk.pmcid,
                #         doi=chunk.doi,
                #         title=chunk.title,
                #         authors=chunk.authors,
                #         journal=chunk.journal,
                #         publication_year=chunk.publication_year,
                #         url=chunk.url
                #     )                    
                # )
                
                seen_sources.add(paper_id)
            
        return ("\n\n".join(context_parts), sources)
        

context_builder = ContextBuilder()

from models.retrieval import RetrievalResult


class ContextBuilder:
    def build_context(
        self,
        results: list[RetrievalResult]
    ) -> str:
        
        context_parts = []
        
        for index, result in enumerate(
            results,
            start = 1
        ):
            chunk = result.chunk
            context_parts.append(
                f"""
                    Source {index}
                    
                    Paper ID: 
                    {    
                        chunk.pmid
                        or chunk.pmcid
                        or chunk.doi
                        or "Unknown"
                    }
                    
                    Text:
                    {chunk.text}
                """
            )
            
        return "\n\n".join(
            context_parts
        )
        

context_builder = ContextBuilder()

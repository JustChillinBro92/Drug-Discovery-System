from models.document_chunk import DocumentChunk
from models.paper_entity import PaperEntity


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 500
    ):
        self.chunk_size = chunk_size
        
    
    def chunk_paper(
        self,
        paper: PaperEntity,
    ) -> list[DocumentChunk]:
        
        # 1. Build the source text
        # 2. Split into chunks (letter/character-based)
        # -------------- TO BE CHANGED -------------- #
        
        text = (
            f"{paper.title}\n\n"
            f"{paper.abstract or ''}"
        )
        
        chunks = []
        
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(
                start + self.chunk_size,
                len(text)
            )
            
            if end < len(text):
                whitespace = text.rfind(
                    " ",
                    start,
                    end
                )
                
                if whitespace != -1:
                    end = whitespace
            
            chunk_text = text[start:end].strip()
            
            # Create the chunk entity
            
            chunk = DocumentChunk(
                chunk_id=f"{paper.pmid or paper.pmcid or paper.doi}_{chunk_index}",

                pmid=paper.pmid,
                pmcid=paper.pmcid,
                doi=paper.doi,

                chunk_index=chunk_index,
                text=chunk_text
            )
            chunks.append(chunk)
            
            start = end
            
            while start < len(text) and text[start].isspace():
                start += 1
            
            chunk_index += 1
            
        return chunks
    
    
text_chunker = TextChunker()

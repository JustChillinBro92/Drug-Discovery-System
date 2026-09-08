import uuid

from models.conversation_state import LiteratureRetrievalState
from models.pipeline_response import PipelineResponse


class LiteratureResolver:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def run_literature_acquisition(self, request, state):
        page_size = int(input("Enter the amount of papers to retrieve: "))
        papers = self.dependencies.paper_normalizer.normalize(
            request.query,
            page_size=page_size
        )

        total_chunks = 0
        added_papers = 0
        duplicate_papers = 0

        for paper in papers:
            paper_id = paper.pmid or paper.pmcid or paper.doi
            if self.dependencies.vector_store.paper_exists(paper_id):
                duplicate_papers += 1
                continue

            chunks = self.dependencies.text_chunker.chunk_paper(paper)
            embeddings = self.dependencies.embedding_service.embed_chunks(chunks)
            self.dependencies.vector_store.add_documents(chunks, embeddings)
            added_papers += 1
            total_chunks += len(chunks)

        return PipelineResponse(
            mode=request.mode,
            message="Literature indexed successfully!",
            papers_added=added_papers,
            chunks_added=total_chunks,
            duplicate_papers=duplicate_papers
        )


    def run_literature_conversation(self, request, state):
        retrieved_chunks = self.dependencies.retriever.retrieve(request.query)
        context, sources, referenced_papers = (
            self.dependencies.context_builder.build_context(retrieved_chunks)
        )

        unique_papers = []
        for paper in referenced_papers:
            paper_id = paper.pmid or paper.pmcid or paper.doi
            if not paper_id or paper_id not in state.referenced_paper_ids:
                unique_papers.append(paper)
                if paper_id:
                    state.referenced_paper_ids.add(paper_id)

        retrieval_id = str(uuid.uuid4())
        state.literature_retrievals[retrieval_id] = LiteratureRetrievalState(
            query=request.query,
            retrieved_chunk_ids=[
                result.chunk.chunk_id
                for result in retrieved_chunks
            ],
            referenced_papers=unique_papers,
            offset=len(retrieved_chunks)
        )

        answer = self.dependencies.generator.generate(
            context=context,
            query=request.query
        )
        
        return PipelineResponse(
            mode=request.mode,
            answer=answer,
            sources=sources
        )


    def run_view_indexed_papers(self, request, state):
        return PipelineResponse(
            mode=request.mode,
            papers=self.dependencies.vector_store.get_indexed_papers()
        )


    def run_delete_indexed_papers(self, request, state):
        if request.query.lower() == "y":
            self.dependencies.vector_store.clear_collection()
            return PipelineResponse(
                mode=request.mode,
                message="Indexed papers deleted successfully!"
            )

        return PipelineResponse(
            mode=request.mode,
            message="Deletion cancelled."
        )

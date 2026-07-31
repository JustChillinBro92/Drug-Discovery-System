from services.input_understanding import understand_input

from models.pipeline_response import PipelineResponse
from models.conversation_state import ConversationState


class PipelineOrchestrator:

    def __init__(
        self,
        paper_normalizer,
        text_chunker,
        embedding_service,
        faiss_service,
        retriever,
        context_builder,
        generator
    ):
        # Pending
        
        self.paper_normalizer = paper_normalizer
        self.text_chunker = text_chunker
        self.embedding_service = embedding_service
        self.faiss_service = faiss_service
        self.retriever = retriever
        self.context_builder = context_builder
        self.generator = generator


    """
    Main pipeline controller.

    Receives validated user request
    and routes it to the required workflow.
    """


    def run(
        self,
        conversation_id: str,
        mode: str,
        query: str,
        state: ConversationState
    ):

        request = understand_input(
            conversation_id=conversation_id,
            mode=mode,
            query=query
        )


        if request.mode == "literature_acquisition":

            return self.run_literature_acquisition(
                request,
                state
            )


        elif request.mode == "literature_conversation":

            return self.run_literature_conversation(
                request,
                state
            )



        elif request.mode == "molecule_analysis":

            return self.run_molecule_analysis(
                request,
                state
            )


        elif request.mode == "similar_compound_search":

            return self.run_similarity_search(
                request,
                state
            )


        elif request.mode == "drug_likeness":

            return self.run_drug_likeness(
                request,
                state
            )


        elif request.mode == "report_generation":

            return self.run_report_generation(
                request,
                state
            )


        else:
            raise ValueError(
                f"Unsupported mode: {request.mode}"
            )


    def run_literature_acquisition(
        self,
        request,
        state
    ):
        page_size = int(input("Enter the amount of papers to retrieve: "))

        papers = self.paper_normalizer.normalize(
            request.query,
            page_size=page_size
        )
    
        total_chunks = 0
        
        for paper in papers:
            chunks = self.text_chunker.chunk_paper(
                paper
            )
            
            embeddings = self.embedding_service.embed_chunks(
                chunks
            )
            
            self.faiss_service.add_documents(
                chunks,
                embeddings
            )
            
            total_chunks += len(chunks)
            
            
        return PipelineResponse(
            mode = request.mode,
            message = "Literature indexed successfully!",
            papers_added = len(papers),
            chunks_added = total_chunks
        )


    def run_literature_conversation(
        self,
        request,
        state
    ):
        
        retrieved_chunks = self.retriever.retrieve(
            request.query,
        )
        
        context, sources = self.context_builder.build_context(
            retrieved_chunks
        )
        
        answer = self.generator.generate(
            context = context,
            query = request.query
        )

        return PipelineResponse(
            mode = request.mode,
            answer = answer,
            sources = sources
        )


    def run_molecule_analysis(
        self,
        request,
        state
    ):

        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis pipeline pending"
        )


    def run_similarity_search(
        self,
        request,
        state
    ):

        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis pipeline pending"
        )


    def run_drug_likeness(
        self,
        request,
        state
    ):
        
        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis pipeline pending"
        )


    def run_report_generation(
        self,
        request,
        state
    ):
        
        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis pipeline pending"
        )
        

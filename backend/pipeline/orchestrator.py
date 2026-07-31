from services.input_understanding import understand_input

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


        if request.mode == "literature_search":

            return self.run_literature_search(
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




    def run_literature_search(
        self,
        request,
        state
    ):

        # 1. Retrieve papers

        papers = self.paper_normalizer.normalize(
            request.query,
            page_size=100
        )


        # 2. Chunk + Embed + Index

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


        # 3. Retrieve relevant chunks

        retrieved_chunks = self.retriever.retrieve(
            request.query
        )
        
        # for i, result in enumerate(retrieved_chunks, start=1):
        #     print(f"\n===== Chunk {i} =====")
        #     print(result.chunk.text)


        # 4. Build context

        context = self.context_builder.build_context(
            retrieved_chunks
        )


        # 5. Generate answer

        answer = self.generator.generate(
            context=context,
            query=request.query
        )


        return {
            "mode": request.mode,
            "answer": answer
        }




    def run_molecule_analysis(
        self,
        request,
        state
    ):

        return {
            "mode": request.mode,
            "message": "Molecule analysis pipeline pending"
        }


    def run_similarity_search(
        self,
        request,
        state
    ):

        return {
            "mode": request.mode,
            "message": "Similarity search pipeline pending"
        }


    def run_drug_likeness(
        self,
        request,
        state
    ):

        return {
            "mode": request.mode,
            "message": "Drug likeness pipeline pending"
        }


    def run_report_generation(
        self,
        request,
        state
    ):

        return {
            "mode": request.mode,
            "message": "Report generation pipeline pending"
        }
        

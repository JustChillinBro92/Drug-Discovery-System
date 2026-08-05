from services.input_understanding import understand_input

from models.pipeline_response import PipelineResponse
from models.conversation_state import ConversationState
from models.pipeline_response import SourceReference



class PipelineOrchestrator:
    def __init__(
        self,
        paper_normalizer,
        text_chunker,
        embedding_service,
        vector_store,
        retriever,
        context_builder,
        generator,
        compound_normalizer,
        rdkit_service,
        fingerprint_service,
        similarity_search_service
    ):
        # Pending
        
        self.paper_normalizer = paper_normalizer
        self.text_chunker = text_chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.retriever = retriever
        self.context_builder = context_builder
        self.generator = generator
        self.compound_normalizer=compound_normalizer
        self.rdkit_service=rdkit_service
        self.fingerprint_service=fingerprint_service
        self.similarity_search_service=similarity_search_service


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
        state: ConversationState,
        **kwargs
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
            
            
        elif request.mode == "view_indexed_papers":

            return self.run_view_indexed_papers(
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
                state,
                **kwargs
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
        added_papers = 0
        
        
        for paper in papers:
            paper_id = (
                paper.pmid
                or paper.pmcid
                or paper.doi
            )
            
            # Prevents addition of duplicate papers
            
            if self.vector_store.paper_exists(
                paper_id
            ):
                continue
            
            chunks = self.text_chunker.chunk_paper(
                paper
            )
            
            embeddings = self.embedding_service.embed_chunks(
                chunks
            )
            
            self.vector_store.add_documents(
                chunks,
                embeddings
            )
            
            added_papers += 1
            total_chunks += len(chunks)
            
            
            # Keep conversation-specific memory only
            state.referenced_papers.append(
                paper
            )
        
            
        return PipelineResponse(
            mode = request.mode,
            message = "Literature indexed successfully!",
            papers_added = added_papers,
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


    def run_view_indexed_papers(
        self,
        request,
        state
    ):

        papers = self.vector_store.get_indexed_papers()
        
        sources = []
        
        for paper in papers:
            sources.append(
                SourceReference(
                    title=paper.get("title"),
                    pmid=paper.get("pmid"),
                    pmcid=paper.get("pmcid"),
                    doi=paper.get("doi"),
                    journal=paper.get("journal"),
                    publication_year=paper.get("publication_year"),
                    url=paper.get("url")
                )
            )
            
        return PipelineResponse(
            mode=request.mode,
            sources=sources
        )
        

    def run_molecule_analysis(
        self,
        request,
        state
    ):
        
        compound = self.compound_normalizer.normalize(
            request.query
        )
        
        properties = self.rdkit_service.analyze_properties(
            compound
        )
        
        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis completed",
            data = {
                "compound": compound.model_dump(),
                "properties": properties.model_dump()
            }
        )


    def run_similarity_search(
        self,
        request,
        state,
        **kwargs
    ):
        
        query_compound = self.compound_normalizer.normalize(
            request.query
        )
        
        query_compound_fingerprint = self.fingerprint_service.generate_morgan_fingerprint(
            query_compound
        )
        
        target_compound_data = []
        
        for compound in kwargs.get("target_compounds", []):
            nmz_compound = self.compound_normalizer.normalize(
                compound
            )
            
            fingerprint = self.fingerprint_service.generate_morgan_fingerprint(
                nmz_compound
            )
            
            target_compound_data.append(
                {
                    "compound": nmz_compound,
                    "fingerprint": fingerprint 
                }
            )
        
        
        similarity_results = self.similarity_search_service.search_similar_compounds(
            query_compound_fingerprint,
            target_compound_data
        )
        

        return PipelineResponse(
            mode = request.mode,
            message = "Similarity search completed",
            data = {
                "compound": query_compound.model_dump(),
                "similarity_results": similarity_results
            }
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
        

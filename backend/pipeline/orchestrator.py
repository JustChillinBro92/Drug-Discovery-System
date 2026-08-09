from services.input_understanding import understand_input

from models.pipeline_response import PipelineResponse
from models.conversation_state import ConversationState
from models.compound_analysis import CompoundAnalysis
from models.paper_entity import PaperEntity


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
            
        elif request.mode == "delete_indexed_papers":

            return self.run_delete_indexed_papers(
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


        elif request.mode == "report_generation":

            return self.run_report_generation(
                request,
                state
            )


        elif request.mode == "view_conversation_state":
            
            return self.run_view_conversation_state(
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
        duplicate_papers = 0
        
        
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
                duplicate_papers += 1
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
            
    
        return PipelineResponse(
            mode = request.mode,
            message = "Literature indexed successfully!",
            papers_added = added_papers,
            chunks_added = total_chunks,
            duplicate_papers = duplicate_papers
        )


    def run_literature_conversation(
        self,
        request,
        state
    ):
        
        retrieved_chunks = self.retriever.retrieve(
            request.query,
        )
        
        # Store retrieved chunks in conversation state
        
        state.retrieved_chunk_ids = [
            result.chunk.chunk_id
            for result in retrieved_chunks
        ]
        
        
        context, sources, referenced_papers = (
            self.context_builder.build_context(
                retrieved_chunks
            )
        )

        
        # Store papers actually referenced in answer
        
        existing_paper_ids = {
            (
                paper.pmid or
                paper.pmcid or
                paper.doi
            )
            for paper in state.referenced_papers
        }
        
        
        for paper in referenced_papers:
            paper_id = (
                paper.pmid
                or paper.pmcid
                or paper.doi
            )
            
            if paper_id not in existing_paper_ids:
                state.referenced_papers.append(
                    paper
                )

                existing_paper_ids.add(
                    paper_id
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
                    
        return PipelineResponse(
            mode=request.mode,
            papers=papers
        )
        

    def run_delete_indexed_papers(
        self,
        request,
        state
    ):
        
        query_confirm = request.query.lower()
        
        if query_confirm == 'y':
            self.vector_store.clear_collection()
        
            return PipelineResponse(
                mode=request.mode,
                message="Indexed papers deleted successfully!"
            )
        
        return PipelineResponse(
            mode=request.mode,
            message="Deletion cancelled."
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
        
        
        # Update conversation state
        
        existing = {
            c.compound_name
            for c in state.analyzed_compounds
        }
        
        
        if compound.canonical_name not in existing:
            state.analyzed_compounds.append(
                CompoundAnalysis(
                    compound=compound,
                    properties=properties
                )
            )
        
        
        lipinski = properties.lipinski
        
        drug_likeness = {
            "lipinski": {
                "molecular_weight": {
                    "value": properties.molecular_weight,
                    "limit": "≤ 500 Da",
                    "pass": lipinski.molecular_weight_pass,
                    "explanation": (
                        "Molecular weight affects absorption and membrane "
                        "permeability. Compounds with molecular weight above "
                        "500 Da often show reduced oral bioavailability."
                    )
                },

                "logp": {
                    "value": properties.logp,
                    "limit": "≤ 5",
                    "pass": lipinski.logp_pass,
                    "explanation": (
                        "LogP represents lipophilicity. Suitable LogP values "
                        "help balance membrane permeability and aqueous "
                        "solubility. Very high lipophilicity may reduce "
                        "solubility and increase metabolic issues."
                    )
                },

                "hydrogen_bond_donors": {
                    "value": properties.h_bond_donors,
                    "limit": "≤ 5",
                    "pass": lipinski.hbd_pass,
                    "explanation": (
                        "Hydrogen bond donors influence interactions with "
                        "biological targets and affect permeability. Excessive "
                        "donor groups can reduce drug absorption."
                    )
                },

                "hydrogen_bond_acceptors": {
                    "value": properties.h_bond_acceptors,
                    "limit": "≤ 10",
                    "pass": lipinski.hba_pass,
                    "explanation": (
                        "Hydrogen bond acceptors affect molecular interactions "
                        "with proteins and solubility. Excessive acceptors may "
                        "negatively impact permeability and bioavailability."
                    )
                },

                "overall": {
                    "pass": lipinski.overall_pass,
                    "violations": lipinski.violations,
                    "classification": (
                        "Drug-like"
                        if lipinski.overall_pass
                        else "Poor drug-likeness"
                    ),
                    "explanation": (
                        "The compound satisfies all Lipinski Rule of Five "
                        "criteria and shows characteristics commonly associated "
                        "with orally active drug candidates."
                        if lipinski.overall_pass
                        else
                        "The compound violates one or more Lipinski Rule of "
                        "Five criteria, which may indicate reduced suitability "
                        "as an orally active drug candidate."
                    )
                }
            }
        }
        
    
        return PipelineResponse(
            mode = request.mode,
            message = "Molecule analysis completed",
            data = {
                "compound": compound.model_dump(),
                "properties": properties.model_dump(),
                "drug_likeness": drug_likeness
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
        
        query_compound_fingerprint = (
            self.fingerprint_service.generate_morgan_fingerprint(
                query_compound
            )   
        )
        
        target_compound_data = []
        
        for compound in kwargs.get("target_compounds", []):
            nmz_compound = self.compound_normalizer.normalize(
                compound
            )
            
            fingerprint = (
                self.fingerprint_service.generate_morgan_fingerprint(
                    nmz_compound
                )
            )
            
            target_compound_data.append(
                {
                    "compound": nmz_compound,
                    "fingerprint": fingerprint 
                }
            )
        
        
        similarity_results = (
            self.similarity_search_service
            .search_similar_compounds(
                query_fingerprint=query_compound_fingerprint,
                query_name=query_compound.canonical_name,
                compounds=target_compound_data
            )
        )
        
        
        # Update conversation state

        state.similarity_results.extend(
            similarity_results
        )
        

        return PipelineResponse(
            mode = request.mode,
            message = "Similarity search completed",
            data = {
                "compound": query_compound.model_dump(),
                "similarity_results": similarity_results
            }
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
        

    def run_view_conversation_state(
        self,
        request,
        state
    ):
        
        return PipelineResponse(
            mode = request.mode,
            message = "Current conversation state",
            data = { 
                "state": state.model_dump()
            }
        )
        
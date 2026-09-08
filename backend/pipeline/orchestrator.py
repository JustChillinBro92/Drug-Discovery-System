from services.input_understanding import understand_input

from models.conversation_state import ConversationState
from pipeline.resolvers.dependencies import PipelineDependencies
from pipeline.resolvers.literature_resolver import LiteratureResolver
from pipeline.resolvers.molecular_resolver import MolecularResolver
from pipeline.resolvers.graph_resolver import GraphResolver
from pipeline.resolvers.state_resolver import StateResolver


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
        target_analyzer,
        uniprot_service,
        protein_normalizer,
        compound_normalizer,
        unichem_normalizer,
        disease_normalizer,
        sider_service,
        rdkit_service,
        fingerprint_service,
        similarity_search_service,
        graph_service
    ):
        dependencies = PipelineDependencies(
            paper_normalizer=paper_normalizer,
            text_chunker=text_chunker,
            embedding_service=embedding_service,
            vector_store=vector_store,
            retriever=retriever,
            context_builder=context_builder,
            generator=generator,
            target_analyzer=target_analyzer,
            uniprot_service=uniprot_service,
            protein_normalizer=protein_normalizer,
            compound_normalizer=compound_normalizer,
            unichem_normalizer=unichem_normalizer,
            disease_normalizer=disease_normalizer,
            sider_service=sider_service,
            rdkit_service=rdkit_service,
            fingerprint_service=fingerprint_service,
            similarity_search_service=similarity_search_service,
            graph_service=graph_service
        )

        literature_resolver = LiteratureResolver(dependencies)
        state_resolver = StateResolver()
        graph_resolver = GraphResolver(dependencies)
        molecular_resolver = MolecularResolver(
            dependencies,
            state_resolver,
            graph_resolver
        )

        self._resolvers = {
            "literature_acquisition": literature_resolver.run_literature_acquisition,
            "literature_conversation": literature_resolver.run_literature_conversation,
            "view_indexed_papers": literature_resolver.run_view_indexed_papers,
            "delete_indexed_papers": literature_resolver.run_delete_indexed_papers,
            "molecule_analysis": molecular_resolver.run_molecule_analysis,
            "similar_compound_search": molecular_resolver.run_similarity_search,
            "report_generation": state_resolver.run_report_generation,
            "fetch_from_conversation_state": state_resolver.run_fetch_from_conversation_state,
            "view_conversation_state": state_resolver.run_view_conversation_state
        }

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
        
        resolver = self._resolvers.get(request.mode)
        if resolver is None:
            raise ValueError(f"Unsupported mode: {request.mode}")
        
        return resolver(request, state, **kwargs)

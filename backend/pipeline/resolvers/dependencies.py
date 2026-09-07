from dataclasses import dataclass


@dataclass
class PipelineDependencies:
    paper_normalizer: object
    text_chunker: object
    embedding_service: object
    vector_store: object
    retriever: object
    context_builder: object
    generator: object
    target_analyzer: object
    uniprot_service: object
    protein_normalizer: object
    compound_normalizer: object
    unichem_normalizer: object
    disease_normalizer: object
    sider_service: object
    rdkit_service: object
    fingerprint_service: object
    similarity_search_service: object
    graph_service: object

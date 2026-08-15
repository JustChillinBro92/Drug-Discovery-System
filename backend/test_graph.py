from graph.graph_service import graph_service

from models.biomedical_entities import (
    CompoundEntity,
    ProteinEntity,
    DiseaseEntity,
    SideEffectEntity
)


compound1 = CompoundEntity(
    original_text="Aspirin",
    canonical_name="ASPIRIN_TEST",
    confidence=1.0,
    synonyms=[],
    chembl_id="TEST_CHEMBL_001",
    smiles="CC(=O)Oc1ccccc1C(=O)O",
    inchikey="TEST_INCHIKEY",
    molecular_formula="C9H8O4"
)

compound2 = CompoundEntity(
    original_text="Acetaminophen",
    canonical_name="ACETAMINOPHEN",
    confidence=1.0,
    synonyms=[],
    chembl_id="CHEMBL112",
    smiles="CC(=O)NC1=CC=C(C=C1)O",
    inchikey="RZVAJINKPMORJF-UHFFFAOYSA-N",
    molecular_formula="C8H9NO2"
)


protein = ProteinEntity(
    original_text="EGFR",
    canonical_name="EGFR_TEST",
    confidence=1.0,
    synonyms=[],
    uniprot_id="TEST_P00533",
    gene_symbol="EGFR",
    protein_name="Epidermal Growth Factor Receptor",
    organism="Homo sapiens"
)


disease = DiseaseEntity(
    original_text="Cancer",
    canonical_name="CANCER_TEST",
    confidence=1.0,
    synonyms=[],
    disease_id="TEST_DISEASE_001"
)


side_effect = SideEffectEntity(
    original_text="Nausea",
    canonical_name="NAUSEA_TEST",
    confidence=1.0,
    synonyms=[],
    sider_id="TEST_SIDER_001"
)


try:

    print("Adding nodes...")

    graph_service.add_compound(compound1)
    graph_service.add_compound(compound2)

    graph_service.add_protein(protein)
    graph_service.add_disease(disease)
    graph_service.add_side_effect(side_effect)


    print("Nodes added.")

    print("Adding relationships...")

    graph_service.add_compound_binds_protein(
        compound1,
        protein
    )

    graph_service.add_compound_treats_disease(
        compound1,
        disease
    )

    graph_service.add_compound_causes_side_effect(
        compound1,
        side_effect
    )
    
    graph_service.add_compound_similarity(
        query_compound=compound1,
        target_compound=compound2,
        similarity_score=0.2222
    )

    print("Relationships added.")

    input(
        "\nCheck Neo4j. Press Enter to delete test data..."
    )

finally:

    graph_service.delete_compound(
        compound1.chembl_id
    )

    graph_service.delete_protein(
        protein.uniprot_id
    )

    graph_service.delete_disease(
        disease.disease_id
    )

    graph_service.delete_side_effect(
        side_effect.sider_id
    )

    print("Test data deleted.")

    graph_service.close()
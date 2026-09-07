import json

# from llm.gemini_client import GeminiClient
# from llm.generator import Generator

# from services.sources.chembl_service import chembl_service
# from services.sources.unichem_service import unichem_service
# from services.sources.sider_service import sider_service
# from services.sources.chembl_service import ChEMBLService
# from services.analyzers.chembl_target_analyzer import ChEMBLTargetAnalyzer

# from services.sources.uniprot_service import uniprot_service
# from services.sources.europepmc_service import europepmc_service

# from services.normalizers.compound_normalizer import compound_normalizer
# from services.normalizers.unichem_normalizer import unichem_normalizer
# from services.normalizers.paper_normalizer import paper_normalizer
# from services.normalizers.protein_normalizer import protein_normalizer
from services.normalizers.disease_normalizer import disease_normalizer

# from services.analyzers.rdkit_service import rdkit_service
# from services.analyzers.fingerprint_service import fingerprint_service
# from services.analyzers.similarity_service import similarity_service
# from services.analyzers.similarity_search_service import similarity_search_service

# from rag.text_chunker import text_chunker
# from rag.embedding_service import embedding_service
# from rag.vector_store import vector_store
# from rag.retriever import retriever

# result = chembl_service.search_compound("Aspirin")


# print("SEARCH RESULT")
# print(result)


# molecule = chembl_service.get_molecule(
#     "CHEMBL25"
# )


# print("\nMOLECULE DETAILS")
# print(molecule)


# molecule = unichem_service.get_compound_sources(
#     "CHEMBL25"
# )

# print("\nMOLECULE DETAILS")
# print(molecule.get("compounds")[0].get("sources")[0])

# nmz_compound = unichem_normalizer.normalize(
#     "CHEMBL424"
# )

# side_effects = sider_service.get_side_effects(
#     nmz_compound.get("pubchem_cids")
# )

# print(len(side_effects))

# compound1 = compound_normalizer.normalize("Aspirin")
# compound2 = compound_normalizer.normalize("Ibuprofen")
# compound3 = compound_normalizer.normalize("Paracetamol")
# compound4 = compound_normalizer.normalize("Montelukast")


# print(
#     json.dumps(
#         compound1.model_dump(),
#         indent=4
#     )
# )

# print()

# print(
#     json.dumps(
#         compound2.model_dump(),
#         indent=4
#     )
# )

# print()

# print("Name:", compound1.canonical_name)
# print("ChEMBL ID:", compound1.chembl_id)
# print("SMILES:", compound1.smiles)
# print("Formula:", compound1.molecular_formula)


# print(rdkit_service.validate_compound(compound1))

# properties = rdkit_service.analyze_properties(compound1)

# print(
#     json.dumps(
#         properties.model_dump(),
#         indent=4
#     )
# )

# fingerprint1 = fingerprint_service.generate_morgan_fingerprint(compound1)
# fingerprint2 = fingerprint_service.generate_morgan_fingerprint(compound2)
# fingerprint3 = fingerprint_service.generate_morgan_fingerprint(compound3)
# fingerprint4 = fingerprint_service.generate_morgan_fingerprint(compound4)



# print(fingerprint1)

# print("Algorithm:", fingerprint1.algorithm)

# print("Radius:", fingerprint1.radius)

# print("Bits:", fingerprint1.n_bits)

# print(
#     "Fingerprint length:",
#     len(fingerprint1.fingerprint)
# )

# print(
#     "Number of active bits:",
#     sum(fingerprint1.fingerprint)
# )

# similarity = similarity_service.calculate_similarity(
#     fingerprint1,
#     fingerprint2,
#     compound2.canonical_name
# )

# print(
#     json.dumps(
#         similarity.model_dump(),
#         indent=4
#     )
# )


# compound_database = [
#     {
#         "compound": compound2,
#         "fingerprint": fingerprint2
#     },
#     {
#         "compound": compound3,
#         "fingerprint": fingerprint3
#     },
#     {
#         "compound": compound4,
#         "fingerprint": fingerprint4
#     }
# ]

# results = similarity_search_service.search_similar_compounds(
#     fingerprint1,
#     compound_database,
# )

# for result in results:
#     print(
#             json.dumps(
#             result.model_dump(),
#             indent=4
#         )
#     )


# epmc_papers = europepmc_service.search_service(
#     "Aspirin",
#     page_size=5 
# )

# print(epmc_papers.keys())
# print(epmc_papers["hitCount"])
# print(
#     json.dumps(
#         epmc_papers["resultList"],
#         indent=4
#     )
# )

# nmz_epmc_papers = paper_normalizer.normalize(
#     "Aspirin",
#     page_size=20 
# )

# for paper in nmz_epmc_papers:
#     print(
#         json.dumps(
#             paper.model_dump(),
#             indent=4
#         )
#     )

# for paper in nmz_epmc_papers:
#     chunks = text_chunker.chunk_paper(
#         paper
#     )
    
#     print("\nNew Paper:\n")
    
#     for chunk in chunks:
#         print(
#             json.dumps(
#                 chunk.model_dump(),
#                 indent=4
#             )
#         )


# for paper in nmz_epmc_papers:
#     chunks = text_chunker.chunk_paper(
#         paper
#     )
    
#     embeddings = embedding_service.embed_chunks(
#         chunks
#     )
    
#     vector_store.add_documents(
#         chunks,
#         embeddings
#     )
    

# results = retriever.retrieve(
#     query = "How does aspirin affect clotting?",
#     top_k = 5
# )

# for result in results:
#     print(
#         json.dumps(
#             result.model_dump(),
#             indent=4
#         )
#     )

# gemini_client = GeminiClient()

# generator = Generator(
#     client=gemini_client
# )

# chembl_service = ChEMBLService()
# target_analyzer = ChEMBLTargetAnalyzer(
#     generator=generator,
# )


# activities = chembl_service.get_activities("CHEMBL25")

# for activity in activities:
#     if activity.get("activity_id") == 42173:
#         print(activity)


# proteins = target_analyzer.get_protein_targets_for_molecule(
#     "CHEMBL3707395"
# )

# for protein in proteins:
#     print(
#         f"\nTarget ID: {protein['target_chembl_id']}"
#         f"\nTarget: {protein['target_name']}"
#         f"\nOrganism: {protein['organism']}"
#         f"\nAccession: {protein['accession']}"
#         f"\nDescription: {protein['component_description']}"
#         f"\nType: {protein['component_type']}"
#         f"\nInteraction: {protein['interaction_type']}"
#         f"\nActivities: {len(protein['activities'])}"
#     )
    

    # for activity in protein["activities"]:
    #     print(
    #         f"\nActivity ID: "
    #         f"{activity['activity_id']}"
    #     )
    #     print(
    #         f"Type: "
    #         f"{activity['standard_type']}"
    #     )
    #     print(
    #         f"Value: "
    #         f"{activity['standard_value']} "
    #         f"{activity['standard_units']}"
    #     )
    #     print(
    #         f"Assay: "
    #         f"{activity['assay_chembl_id']}"
    #     )
    #     print(
    #         f"Year: "
    #         f"{activity['document_year']}"
    #     )
        
    # protein_details = uniprot_service.get_protein(
    #     protein['accession']
    # )
    
    # nmz_protein = protein_normalizer.normalize(
    #     protein_details,
    #     protein["organism"]
    # )
    
    # print(
    #     f"\nUniProt ID: {nmz_protein.uniprot_id}"
    #     f"\nProtein Name: {nmz_protein.protein_name}"
    #     f"\nGene Symbol: {nmz_protein.gene_symbol}"
    #     # f"\nOrganism: {nmz_protein.organism}"
    #     # f"\nFunction: {nmz_protein.function}"
    #     # f"\nSubcellular Location: {nmz_protein.subcellular_location}"
    #     # f"\nPathways: {nmz_protein.pathways}"
    #     # f"\nSequence: {nmz_protein.sequence}"
    #     # f"\nSequence Length: {nmz_protein.sequence_length}"
    # )
        
        
# test_ids = [
#     "CHEMBL25",      # Aspirin
#     "CHEMBL521",     # Ibuprofen
#     "CHEMBL112",     # Paracetamol
#     "CHEMBL113",     # Caffeine
#     "CHEMBL154"      # Naproxen
# ]

# for molecule_id in test_ids:

#     print(f"\n{'=' * 50}")
#     print(f"Molecule: {molecule_id}")
#     print(f"{'=' * 50}")

#     proteins = chembl_service.get_protein_targets_for_molecule(
#         molecule_id
#     )

#     print(f"Protein targets: {len(proteins)}")

#     for protein in proteins:
#         print(
#             protein["target_chembl_id"],
#             "|",
#             protein["target_name"],
#             "|",
#             protein["organism"],
#             "|",
#             protein["accession"]
#         )


# rxcui = disease_normalizer.normalize_compound(
#     "aspirin"
# )

# diseases = disease_normalizer.normalize_disease(rxcui)

# print(diseases)
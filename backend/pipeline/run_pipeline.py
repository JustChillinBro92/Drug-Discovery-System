import json

from models.conversation_state import ConversationState

from pipeline.orchestrator import PipelineOrchestrator


from rag.text_chunker import text_chunker
from rag.embedding_service import embedding_service
from rag.vector_store import vector_store
from rag.retriever import retriever
from rag.context_builder import context_builder

from llm.gemini_client import GeminiClient
from llm.generator import Generator

from services.analyzers.chembl_target_analyzer import ChEMBLTargetAnalyzer
from services.normalizers.compound_normalizer import compound_normalizer
from services.normalizers.unichem_normalizer import unichem_normalizer
from services.normalizers.disease_normalizer import disease_normalizer

from services.normalizers.protein_normalizer import protein_normalizer
from services.normalizers.paper_normalizer import paper_normalizer

from services.analyzers.rdkit_service import rdkit_service
from services.analyzers.fingerprint_service import fingerprint_service
from services.analyzers.similarity_search_service import similarity_search_service
from services.sources.uniprot_service import uniprot_service
from services.sources.sider_service import sider_service

from graph.graph_service import graph_service


# Initialize dependencies

gemini_client = GeminiClient()
generator = Generator(
    client=gemini_client
)

target_analyzer = ChEMBLTargetAnalyzer(
    generator=generator
)

# Inject dependencies into orchestrator (Pending)

orchestrator = PipelineOrchestrator(
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


# Pipeline execution entry point

def execute(
    conversation_id: str,
    mode: str,
    query: str,
    state: ConversationState,
    **kwargs
):

    return orchestrator.run(
        conversation_id=conversation_id,
        mode=mode,
        query=query,
        state=state,
        **kwargs
    )


# Terminal testing

if __name__ == "__main__":

    from models.conversation_state import ConversationState


    conversation_id = "terminal_session_001"

    state = ConversationState(
        conversation_id=conversation_id
    )


    while True:
        print()
        print("1. Literature Acquisition")
        print("2. Literature Conversation")
        print("3. View Indexed Papers")
        print("4. Delete Indexed Papers")
        print("5. Molecule Analysis")
        print("6. Similar Compound Search")
        print("7. Report Generation")
        print("8. Fetch From Conversation State")
        print("9. View Conversation State")
        print("0. Exit")


        choice = input("\nChoice: ")


        if choice == "0":
            vector_store.close()
            break


        modes = {
            "1": "literature_acquisition",
            "2": "literature_conversation",
            "3": "view_indexed_papers",
            "4": "delete_indexed_papers",
            "5": "molecule_analysis",
            "6": "similar_compound_search",
            "7": "report_generation",
            "8": "fetch_from_conversation_state",
            "9": "view_conversation_state",
        }


        if choice not in modes:
            print("Invalid mode")
            continue


        mode = modes[choice]
        
        if mode == "view_indexed_papers":
            result = execute(
                conversation_id=conversation_id,
                mode=mode,
                query="",
                state=state
            )
            
        elif mode == "delete_indexed_papers":
            query_confirm = input("\nDelete all indexed papers? (y/n): ")
            
            result = execute(
                conversation_id=conversation_id,
                mode=mode,
                query=query_confirm,
                state=state
            )
            
        elif mode == "similar_compound_search":
            query_compound = input("\nEnter query compound: ")
            target_compounds = input("\nEnter target compounds(separated by ','): ")
            
            target_compound_list = [
                compound.strip()
                for compound in target_compounds.split(",")
            ]
            
            result = execute(
                conversation_id=conversation_id,
                mode=mode,
                query=query_compound,
                state=state,
                target_compounds=target_compound_list
            )
           
        elif mode == "view_conversation_state":
            result = execute(
                conversation_id=conversation_id,
                mode=mode,
                query="",
                state=state
            )
         
        else:

            query = input("\nQuery: ")

            result = execute(
                conversation_id=conversation_id,
                mode=mode,
                query=query,
                state=state
            )


        print(f"\n{'=' * 21} RESPONSE {'=' * 21}")

        print(f"\nMode: {result.mode}")

        if result.answer:
            print()
            print("+--------+")
            print("| Answer |")
            print("+--------+")
            print(result.answer)
         
           
        if result.data:
            print("\nDetails:")
            
            data = result.data

            if "compound" in data:
                compound = data["compound"]

                print()
                print("+----------------------+")
                print("| Compound Information |")
                print("+----------------------+")

                print(f"Original Input       : {compound.get('original_text')}")
                print(f"Canonical Name       : {compound.get('canonical_name')}")
                print(f"Confidence           : {compound.get('confidence')}")
                # print(f"Synonyms             : {', '.join(compound.get('synonyms', [])) or 'None'}")
                print(f"ChEMBL ID            : {compound.get('chembl_id')}")
                print(f"SMILES               : {compound.get('smiles')}")
                print(f"InChIKey             : {compound.get('inchikey')}")
                print(f"Molecular Formula    : {compound.get('molecular_formula')}")              
                
                
            if "properties" in data:
                properties = data["properties"]

                print()
                print("+------------+")
                print("| Properties |")
                print("+------------+")
                
                
                print(f"Molecular Weight     : {properties.get('molecular_weight')} Da")
                print(f"LogP                 : {properties.get('logp')}")
                print(f"TPSA                 : {properties.get('tpsa')} Å²")
                print(f"H-Bond Donors        : {properties.get('h_bond_donors')}")
                print(f"H-Bond Acceptors     : {properties.get('h_bond_acceptors')}")
                print(f"Rotatable Bonds      : {properties.get('rotatable_bonds')}")
                print(f"Heavy Atom Count     : {properties.get('heavy_atom_count')}")
                print(f"Ring Count           : {properties.get('ring_count')}")
                print(f"Aromatic Ring Count  : {properties.get('aromatic_ring_count')}")
                print(f"Formal Charge        : {properties.get('formal_charge')}")
                print(f"Fraction CSP3        : {properties.get('fraction_csp3')}")
                print(f"QED                  : {properties.get('qed')}")

                 
            if "drug_likeness" in data:
                print()
                print("+---------------+")
                print("| Drug Likeness |")
                print("+---------------+")
                
                lipinski = data["drug_likeness"]["lipinski"]
                
                print("Lipinski's Rule of Five:")

                mw = lipinski["molecular_weight"]
                print("\nMolecular Weight")
                print("------------------")
                print(f"Value : {mw['value']} Da")
                print(f"Limit : {mw['limit']}")
                print(f"Pass  : {mw['pass']}")
                
                print(f"\nExplanation:")
                print(f"{mw['explanation']}")


                logp = lipinski["logp"]
                print("\nLogP")
                print("------")
                print(f"Value : {logp['value']}")
                print(f"Limit : {logp['limit']}")
                print(f"Pass  : {logp['pass']}")
                
                print(f"\nExplanation:")
                print(f"{logp['explanation']}")


                hbd = lipinski["hydrogen_bond_donors"]
                print("\nHydrogen Bond Donors (HBD)")
                print("----------------------------")
                print(f"Value : {hbd['value']}")
                print(f"Limit : {hbd['limit']}")
                print(f"Pass  : {hbd['pass']}")
                
                print(f"\nExplanation:")
                print(f"{hbd['explanation']}")


                hba = lipinski["hydrogen_bond_acceptors"]
                print("\nHydrogen Bond Acceptors (HBA)")
                print("-------------------------------")
                print(f"Value : {hba['value']}")
                print(f"Limit : {hba['limit']}")
                print(f"Pass  : {hba['pass']}")
                
                print(f"\nExplanation:")
                print(f"{hba['explanation']}")


                overall = lipinski["overall"]

                print("\nOverall Lipinski Result")
                print("-------------------------")
                print(f"Pass           : {overall['pass']}")
                print(f"Violations     : {overall['violations']}")
                print(f"Classification : {overall['classification']}")
                
                print(f"\nExplanation:")
                print(f"{overall['explanation']}")
              
              
            if "proteins" in data:
                proteins = data["proteins"]
                
                print()
                print("+----------------------+")
                print("| Protein Information  |")
                print("+----------------------+")

                for index, protein in enumerate(proteins, start=1):
                    print(f"\nProtein [{index}]")
                    print("+-------------+")
                    print(f"Target ID             : {protein.get('target_chembl_id')}")
                    print(f"Target                : {protein.get('target_name')}")
                    print(f"Organism              : {protein.get('organism')}")
                    print(f"Accession             : {protein.get('accession')}")
                    print(f"Description           : {protein.get('component_description')}")
                    print(f"Type                  : {protein.get('component_type')}")
                    print(f"Interaction           : {protein.get('interaction_type')}")
                    print(f"Activities            : {protein.get('activities_no')}")

                    nmz_protein = protein.get("protein", {})                       
                        
                    print()
                    print(f"UniProt ID            : {nmz_protein.get('uniprot_id')}")
                    print(f"Protein Name          : {nmz_protein.get('protein_name')}")
                    print(f"Gene Symbol           : {nmz_protein.get('gene_symbol')}")
                    # print(f"Function              : {nmz_protein.get('function')}")
                    print(f"Subcellular Location  : {nmz_protein.get('subcellular_location')}")
                    print(f"Pathways              : {nmz_protein.get('pathways')}")
                    print(f"Sequence              : {nmz_protein.get('sequence')}")                    
                    print(f"Sequence Length       : {nmz_protein.get('sequence_length')}")


            if "side_effects" in data:
                side_effects = data["side_effects"]

                print()
                print("+----------------------------+")
                print("| Potential Side Effects     |")
                print("+----------------------------+")

                for index, side_effect in enumerate(side_effects, start=1):
                    print(f"\nSide Effect [{index}]")
                    print(f"MedDRA ID    : {side_effect.meddra_id}")
                    print(f"Name         : {side_effect.side_effect_name}")
                    print(f"MedDRA Level : {side_effect.meddra_level}")


            if "diseases" in data:
                diseases = data["diseases"]

                print()
                print("+-----------------------+")
                print("| Potentially Treats    |")
                print("+-----------------------+")

                for index, disease in enumerate(diseases, start=1):
                    print(f"\nDisease [{index}]")
                    print(f"Mesh ID            : {disease.mesh_id}")
                    print(f"Mesh Concept ID    : {disease.mesh_concept_id}")
                    print(f"Name               : {disease.disease_name}")
                    print(f"Description        : {disease.description}")

                    
            if "similarity_results" in data:
                compounds = data["similarity_results"]
                
                print()
                print("+--------------------+")
                print("| Similarity Results |")
                print("+--------------------+")
                
                for compound in compounds:
                    print(f"Query Compound       : {compound.query_compound}")
                    print(f"Compared Compound    : {compound.compound_name}")
                    print(f"ChEMBL ID            : {compound.chembl_id}")
                    print(f"Similarity Score     : {compound.similarity_score}\n")


            if "retrieved_state" in data:
                retrieval = data["retrieved_state"]

                print()
                print("+-------------------------+")
                print("| Literature Retrieval    |")
                print("+-------------------------+")

                print(f"Query    : {retrieval.get('query')}")
                print(f"Category : {retrieval.get('category')}")
                print(f"Offset   : {retrieval.get('offset')}")

                print("\nRetrieved Chunk IDs:")
                for chunk_id in retrieval.get(
                    "retrieved_chunk_ids", []
                ):
                    print(f"- {chunk_id}")

                print("\nReferenced Papers:")
                for paper in retrieval.get(
                    "referenced_papers", []
                ):
                    print(paper)


            if "state" in data:
                state_data = data["state"]

                print()
                print("+--------------------+")
                print("| Conversation State |")
                print("+--------------------+")

                print(f"Conversation ID : {state_data.get('conversation_id')}")
                print(f"Current Mode    : {state_data.get('current_mode')}")

                print("\nEntities:")
                print(state_data.get("entities"))

                print("\nAnalyzed Compounds:")
                for compound in state_data.get("analyzed_compounds", []):
                    print(compound)

                print("\nSimilarity Results:")
                for similarity_result in state_data.get("similarity_results", []):
                    print(similarity_result)

                print("\nLiterature Retrievals:")

                for retrieval_id, retrieval in state_data.get(
                    "literature_retrievals", {}
                ).items():

                    print(f"\nRetrieval ID : {retrieval_id}")
                    print(f"Query       : {retrieval.get('query')}")
                    print(f"Category    : {retrieval.get('category')}")
                    print(f"Offset      : {retrieval.get('offset')}")

                    print("\nRetrieved Chunk IDs:")
                    for chunk_id in retrieval.get(
                        "retrieved_chunk_ids", []
                    ):
                        print(f"- {chunk_id}")

                    print("\nReferenced Papers:")
                    for paper in retrieval.get(
                        "referenced_papers", []
                    ):
                        print(paper)

                print("\nReferenced Paper IDs:")
                for paper_id in state_data.get(
                    "referenced_paper_ids", []
                ):
                    print(f"- {paper_id}")

                print("\nImportant Context:")
                for context in state_data.get(
                    "important_context", []
                ):
                    print(f"- {context}")
                            

        if result.message:
            print("\nMessage:")
            print(result.message)


        if result.papers_added is not None:
            print(f"\nPapers Added: {result.papers_added}")


        if result.chunks_added is not None:
            print(f"Chunks Added: {result.chunks_added}")


        if result.duplicate_papers is not None:
            print(f"Duplicate Papers Retrieved: {result.duplicate_papers}")

            
        if result.sources:
            print("\nSources:")

            for index, source in enumerate(result.sources, start=1):

                print(f"\n[{index}]")

                print(f"Title   : {source.title}")
                print(f"ChunkID : {source.chunk_id}")
                print(f"PMID    : {source.pmid}")
                print(f"PMCID   : {source.pmcid}")
                print(f"DOI     : {source.doi}")
                print(f"Journal : {source.journal}")
                print(f"Year    : {source.publication_year}")
                print(f"URL     : {source.url}")


        if result.papers:
            print("\nIndexed Papers:")

            for index, paper in enumerate(result.papers, start=1):

                print(f"\n[{index}]")

                print(f"Title   : {paper.title}")
                print(f"PMID    : {paper.pmid}")
                print(f"PMCID   : {paper.pmcid}")
                print(f"DOI     : {paper.doi}")
                print(f"Journal : {paper.journal}")
                print(f"Year    : {paper.publication_year}")
                print(f"URL     : {paper.url}")

                # if paper.abstract:
                #     print("\nAbstract:")
                #     print(paper.abstract)   
                         

        print(f"\n{'=' * 52}")
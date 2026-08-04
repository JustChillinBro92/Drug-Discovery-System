import json

from pipeline.orchestrator import PipelineOrchestrator

from services.normalizers.paper_normalizer import paper_normalizer

from rag.text_chunker import text_chunker
from rag.embedding_service import embedding_service
from rag.faiss_service import faiss_service
from rag.retriever import retriever
from rag.context_builder import context_builder

from services.normalizers.compound_normalizer import compound_normalizer
from services.analyzers.rdkit_service import rdkit_service
from services.analyzers.fingerprint_service import fingerprint_service
from services.analyzers.similarity_search_service import similarity_search_service

from llm.gemini_client import GeminiClient
from llm.generator import Generator


# Initialize dependencies

gemini_client = GeminiClient()
generator = Generator(
    client=gemini_client
)


# Inject dependencies into orchestrator (Pending)

orchestrator = PipelineOrchestrator(
    paper_normalizer=paper_normalizer,
    text_chunker=text_chunker,
    
    embedding_service=embedding_service,
    faiss_service=faiss_service,
    
    retriever=retriever,
    context_builder=context_builder,
    generator=generator,
    
    compound_normalizer=compound_normalizer,
    rdkit_service=rdkit_service,
    fingerprint_service=fingerprint_service,
    
    similarity_search_service=similarity_search_service
)


# Pipeline execution entry point

def execute(
    conversation_id: str,
    mode: str,
    query: str,
    state,
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
        print("4. Molecule Analysis")
        print("5. Similar Compound Search")
        print("6. Drug Likeness")
        print("7. Report Generation")
        print("0. Exit")


        choice = input("\nChoice: ")


        if choice == "0":
            break


        modes = {
            "1": "literature_acquisition",
            "2": "literature_conversation",
            "3": "view_indexed_papers",
            "4": "molecule_analysis",
            "5": "similar_compound_search",
            "6": "drug_likeness",
            "7": "report_generation"
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
            print("\nAnswer:")
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


                if properties.get("lipinski"):
                    lipinski = properties["lipinski"] 
                    
                    lipinski = properties["lipinski"]

                    print()
                    print("+-------------------------+")
                    print("| Lipinski's Rule of Five |")
                    print("+-------------------------+")

                    print(f"Molecular Weight ≤ 500 : {lipinski.get('molecular_weight_pass')}")
                    print(f"LogP ≤ 5               : {lipinski.get('logp_pass')}")
                    print(f"HBD ≤ 5                : {lipinski.get('hbd_pass')}")
                    print(f"HBA ≤ 10               : {lipinski.get('hba_pass')}")
                    print(f"Overall Pass           : {lipinski.get('overall_pass')}")
                    print(f"Violations             : {lipinski.get('violations')}")
                
            if "similarity_results" in data:
                compounds = data["similarity_results"]
                
                print()
                print("+--------------------+")
                print("| Similarity Results |")
                print("+--------------------+")
                
                for compound in compounds:
                    print(f"Canonical Name       : {compound.compound_name}")
                    print(f"ChEMBL ID            : {compound.chembl_id}")
                    print(f"Similarity Score     : {compound.similarity_score}\n")

            
        if result.message:
            print("\nMessage:")
            print(result.message)


        if result.papers_added is not None:
            print(f"\nPapers Added: {result.papers_added}")


        if result.chunks_added is not None:
            print(f"Chunks Added: {result.chunks_added}")


        if result.sources:
            print("\nSources:")

            for index, source in enumerate(result.sources, start=1):

                print(f"\n[{index}]")

                print(f"Title   : {source.title}")
                print(f"PMID    : {source.pmid}")
                print(f"PMCID   : {source.pmcid}")
                print(f"DOI     : {source.doi}")
                print(f"Journal : {source.journal}")
                print(f"Year    : {source.publication_year}")
                print(f"URL     : {source.url}")


        print(f"\n{'=' * 52}")
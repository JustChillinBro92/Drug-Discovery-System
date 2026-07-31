from pipeline.orchestrator import PipelineOrchestrator

from services.normalizers.paper_normalizer import paper_normalizer

from rag.text_chunker import text_chunker
from rag.embedding_service import embedding_service
from rag.faiss_service import faiss_service
from rag.retriever import retriever
from rag.context_builder import context_builder

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
    generator=generator
)


# Pipeline execution entry point

def execute(
    conversation_id: str,
    mode: str,
    query: str,
    state
):

    return orchestrator.run(
        conversation_id=conversation_id,
        mode=mode,
        query=query,
        state=state
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
        print("3. Molecule Analysis")
        print("4. Similar Compound Search")
        print("5. Drug Likeness")
        print("6. Report Generation")
        print("0. Exit")


        choice = input("\nChoice: ")


        if choice == "0":
            break


        modes = {
            "1": "literature_acquisition",
            "2": "literature_conversation",
            "3": "molecule_analysis",
            "4": "similar_compound_search",
            "5": "drug_likeness",
            "6": "report_generation"
        }


        if choice not in modes:
            print("Invalid mode")
            continue


        query = input("\nQuery: ")


        result = execute(
            conversation_id=conversation_id,
            mode=modes[choice],
            query=query,
            state=state
        )


        print("\n========== RESPONSE ==========")

        print(f"\nMode: {result.mode}")

        if result.answer:
            print("\nAnswer:")
            print(result.answer)
           
            
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

        print("\n==============================")
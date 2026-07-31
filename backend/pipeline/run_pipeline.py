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

# retriever = Retriever()
# context_builder = ContextBuilder()

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

        print("\nSelect Mode:")
        print("1. Literature Search")
        print("2. Molecule Analysis")
        print("3. Similar Compound Search")
        print("4. Drug Likeness")
        print("5. Report Generation")
        print("0. Exit")


        choice = input("\nChoice: ")


        if choice == "0":
            break


        modes = {
            "1": "literature_search",
            "2": "molecule_analysis",
            "3": "similar_compound_search",
            "4": "drug_likeness",
            "5": "report_generation"
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


        print("\nResponse:")
        print(result)
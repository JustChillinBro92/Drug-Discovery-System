import json
from uuid import uuid4

from models.conversation_state import ConversationState

from config.config import settings
from llm.gemini_client import GeminiClient
from llm.tool_router import ToolRouter
from pipeline.resolvers.free_conversation_resolver import FreeConversationResolver
from pipeline.run_pipeline import orchestrator
from rag.vector_store import vector_store


conversation_sessions = {}


def create_session_id() -> str:
    return str(uuid4())


def _get_session(conversation_id: str):
    session = conversation_sessions.get(conversation_id)
    if session is None:
        session = {
            "state": ConversationState(),
            "resolver": FreeConversationResolver(
                tool_router=ToolRouter(
                    client=GeminiClient(
                        api_key=settings.GEMINI_WRAPPER_API_KEY
                    ),
                    generator=None
                ),
                resolvers=orchestrator.resolvers
            )
        }
        conversation_sessions[conversation_id] = session
    return session


def execute(conversation_id: str, query: str):
    session = _get_session(conversation_id)
    
    return session["resolver"].run(
        query=query,
        state=session["state"]
    )


if __name__ == "__main__":
    conversation_id = create_session_id()
    print("\nConversation started. Type 'exit' to stop.")
    print(f"Conversation Id: {conversation_id}")


    try:
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in {"exit", "quit"}:
                break
            if not query:
                continue

            result = execute(conversation_id, query)
            print("\nTool results:")
            print(json.dumps(result.data, indent=2))
    finally:
        vector_store.close()

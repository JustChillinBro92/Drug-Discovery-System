import json
from uuid import uuid4

from models.conversation_state import ConversationState
from api.response_models import ConversationResponse

from config.config import settings

from llm.openai_client import OpenAIClient
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
                    client=OpenAIClient(
                        api_key=settings.OPENAI_WRAPPER_API_KEY
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


def run_user_input(conversation_id, query):
    response = execute(conversation_id, query)
    
    print("\nAI:", response.answer)
    
    # Debug
    print("\nTool results:")
    print(json.dumps(response.data, indent=2))
    
    return ConversationResponse (
        conversation_id = conversation_id,
        mode = response.mode,
        message = response.answer,
        data = response.data
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

            run_user_input(conversation_id, query)
    finally:
        vector_store.close()

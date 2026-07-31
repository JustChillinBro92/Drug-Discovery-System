from llm.gemini_client import GeminiClient

from llm.prompts import (
    SYSTEM_PROMPT,
    RAG_PROMPT
)


class Generator:
    def __init__(
        self,
        client: GeminiClient
    ):

        self.client = client


    def generate(
        self,
        context: str,
        query: str
    ) -> str:

        prompt = RAG_PROMPT.format(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            query=query
        )


        return self.client.generate(
            prompt
        )
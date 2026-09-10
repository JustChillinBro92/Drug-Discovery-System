import json

from llm.gemini_client import GeminiClient

from llm.prompts import (
    SYSTEM_PROMPT_1,
    SYSTEM_PROMPT_2,
    SYSTEM_PROMPT_3,
    RAG_PROMPT,
    ASSAY_INTERACTION_PROMPT,
    LITERATURE_INTERACTION_PROMPT,
    FINAL_RESPONSE_PROMPT
)
from google.genai import types


class Generator:
    def __init__(
        self,
        client: GeminiClient
    ):

        self.client = client

    # Retrieved literature summarization model
    
    def generate(
        self,
        context: str,
        query: str
    ) -> str:

        prompt = RAG_PROMPT.format(
            system_prompt=SYSTEM_PROMPT_1,
            context=context,
            query=query
        )

        return self.client.generate(
            prompt
        )
        
        
    # Compound - Protein interaction type classifier model
    
    def classify_interaction(
        self,
        targets: list
    ) -> dict:

        target_data = []

        for target in targets:
            target_data.append({
                "target_chembl_id":
                    target.get(
                        "target_chembl_id"
                    ),
                "target_name":
                    target.get(
                        "target_name"
                    ),
                "target_type":
                    target.get(
                        "target_type"
                    ),
                "activities":
                    target.get(
                        "activities",
                        []
                    )
            })


        prompt = ASSAY_INTERACTION_PROMPT.format(
            system_prompt=SYSTEM_PROMPT_2,
            targets=json.dumps(
                target_data,
                indent=2
            )
        )


        config = types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        )

        response = self.client.generate(
            prompt,
            config=config
        )
        
        # print(response)

        return json.loads(
            response
        )
        
    
    # Compound - Protein interaction extractor from literature

    def extract_literature_interactions(
        self,
        context: str
    ) -> dict:

        prompt = LITERATURE_INTERACTION_PROMPT.format(
            system_prompt=SYSTEM_PROMPT_3,
            context=context
        )

        response = self.client.generate(
            prompt
        )

        return json.loads(
            response
        )



    def generate_final_response(
        self,
        query: str,
        tool_results: list[dict]
    ) -> str:
        prompt = FINAL_RESPONSE_PROMPT.format(
            query=query,
            tool_results=json.dumps(tool_results, indent=2, default=str)
        )
        return self.client.generate(prompt)
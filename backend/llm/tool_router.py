import time
import json
import re

from models.tool_plan import ToolPlan
from llm.prompts import TOOL_ROUTER_SYSTEM_PROMPT
from google.genai import types


class ToolRouter:
    def __init__(self, client, generator):
        self.client = client
        self.generator = generator

    def plan(self, query: str) -> ToolPlan:
        
        start = time.perf_counter()
        print("\nPlanning...")
        
        config = types.GenerateContentConfig(
            system_instruction=TOOL_ROUTER_SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=256,
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(
                thinking_level="low"
            )
        )
        
        response = self.client.generate(query, config=config)
        
        elapsed = time.perf_counter() - start
        print(f"\nReceived Response in {elapsed:.2f}s")
        
        print("\nParsing...")
        parsed_response = self._parse_json(response)
        print("\nFinished Parsing")
        
        return ToolPlan.model_validate(parsed_response)

    @staticmethod
    def _parse_json(response: str) -> dict:
        cleaned = response.strip()
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned)
        try:
            value = json.loads(cleaned)
        except json.JSONDecodeError as error:
            raise ValueError("Tool router returned invalid JSON") from error

        if not isinstance(value, dict):
            raise ValueError("Tool router response must be a JSON object")
        return value

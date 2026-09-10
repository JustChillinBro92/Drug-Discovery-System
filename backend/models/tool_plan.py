from typing import Any, Literal

from pydantic import BaseModel, Field


ToolName = Literal[
    "literature_acquisition",
    "literature_conversation",
    "view_indexed_papers",
    "delete_indexed_papers",
    "molecule_analysis",
    "similar_compound_search",
    "report_generation",
    "fetch_from_conversation_state",
    "view_conversation_state",
]


class ToolCall(BaseModel):
    name: ToolName
    original_query: str = Field(
        default="",
        description="The original user request that led to this tool call."
    )
    query: str = Field(
        default="",
        description="The value required by the selected tool, not the full user request."
    )
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolPlan(BaseModel):
    tools: list[ToolCall] = Field(min_length=1)

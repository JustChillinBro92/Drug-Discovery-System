from api.request_models import AnalysisRequest


VALID_MODES = {
    "literature_acquisition",
    "literature_conversation",
    "view_indexed_papers",
    "delete_indexed_papers",
    "molecule_analysis",
    "similar_compound_search",
    "report_generation",
    "view_conversation_state"
}


"""
Validates and structures user input.
"""

def understand_input(
    conversation_id: str,
    mode: str,
    query: str
) -> AnalysisRequest:

    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid mode: {mode}"
        )

    query = query.strip()

    if mode not in (
        "view_indexed_papers", 
        "view_conversation_state"
    ) and not query:
        raise ValueError("Query cannot be empty")

    return AnalysisRequest(
        conversation_id=conversation_id,
        mode=mode,
        query=query
    )
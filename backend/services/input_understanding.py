from api.request_models import AnalysisRequest


VALID_MODES = {
    "literature_acquisition",
    "literature_conversation",
    "molecule_analysis",
    "similar_compound_search",
    "drug_likeness",
    "report_generation"
}


"""
Validates and structures user input.
Does not perform intent detection.
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

    if not query:
        raise ValueError(
            "Query cannot be empty."
        )

    return AnalysisRequest(
        conversation_id=conversation_id,
        mode=mode,
        query=query
    )
from services.input_understanding import understand_input

def run_pipeline(query: str):
    # Understand user query
    parsed_query = understand_input(query)
    
    return {
        "input": query,
        "parsed": parsed_query
    }
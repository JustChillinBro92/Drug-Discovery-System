from pipeline.orchestrator import run_pipeline

def execute(query: str):
    result = run_pipeline(query)
    
    return result
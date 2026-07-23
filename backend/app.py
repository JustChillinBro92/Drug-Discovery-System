from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Drug Discovery RAG API",
    version="1.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Drug Discovery RAG API running..."
    }
    

# Drug Discovery RAG System

A retrieval-augmented drug discovery backend built with FastAPI. The service combines literature retrieval, biomedical data sources, molecular analysis, similarity search, Neo4j graph queries, Qdrant vector storage, and LLM-assisted responses.

## Requirements

- Python 3.10 or newer
- Create `backend/.env`

*env*:
```sh
- APP_NAME=Drug Discovery RAG

- HF_TOKEN=<your_hugging_face_token>
- NEO4J_URI=<your_neo4j_uri>
- NEO4J_USERNAME=<your_neo4j_username>
- NEO4J_PASSWORD=<your_neo4j_password>
- OPENAI_WRAPPER_KEY=<your_groq_openai_key>
- OPENAI_API_KEY=<your_groq_openai_key>
- OPENAI_MODEL=openai/gpt-oss-120b
 
- CHEMBL_API_URL=https://www.ebi.ac.uk/chembl/api/data
- UNICHEM_API_URL=https://www.ebi.ac.uk/unichem/api/v1
- EUROPEPMC_API_URL=https://www.ebi.ac.uk/europepmc/webservices/rest
- UNIPROT_API_URL=https://rest.uniprot.org
- RXNORM_API_URL=https://rxnav.nlm.nih.gov/REST
- RXCLASS_API_URL=https://rxnav.nlm.nih.gov/REST/rxclass
- MESH_RDF_API_URL=https://id.nlm.nih.gov/mesh
```


## Start the Backend

From the repository root, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

Start the FastAPI server from the `backend` directory:

```powershell
Set-Location backend
python -m uvicorn app:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

## Backend Routes

### `GET /`

Returns a basic service status message.

```sh
http GET http://127.0.0.1:8000/
```

### `GET /health`

Checks whether the API is healthy.

```sh
http GET http://127.0.0.1:8000/health
```

### `POST /analyze`

Runs a pipeline operation with a new conversation state for the request.

Request body:

```json
{
  "mode": "molecule_analysis",
  "query": "aspirin"
}
```

Supported modes:

- `literature_acquisition`: retrieve papers for a topic with `page_size`.
- `literature_conversation`: answer a literature question using retrieved context.
- `view_indexed_papers`: list papers indexed in the vector store.
- `delete_indexed_papers`: delete indexed papers after confirmation in the pipeline.
- `molecule_analysis`: analyze a compound with it's protein interactions, probable side effects and potentially treatable diseases.
- `similar_compound_search`: compare a primary compound against `target_compounds`.

Example request:

```sh
http POST http://127.0.0.1:8000/analyze \
  mode=similar_compound_search \
  query=aspirin \
  target_compounds:='["ibuprofen", "paracetamol"]'
```

For literature acquisition, include `page_size` when needed:

```json
{
  "mode": "literature_acquisition",
  "query": "kinase inhibitors in cancer",
  "page_size": 100
}
```

### `POST /c/{conversation_id}`

Sends a query to the free-conversation pipeline. The `conversation_id` identifies the conversation state used by the conversation service.

Request body:

```json
{
  "query": "What are the known side effects of aspirin?"
}
```

Example request:

```sh
http POST http://127.0.0.1:8000/c/demo-conversation \
  query="What are the known side effects of aspirin?"
```

## Project Layout

- `backend/app.py`: FastAPI application entry point.
- `backend/api/`: request models, response models, and HTTP routes.
- `backend/pipeline/`: orchestration for analysis and conversation workflows.
- `backend/rag/`: chunking, embeddings, retrieval, and Qdrant storage.
- `backend/graph/`: Neo4j client and graph operations.
- `backend/services/`: external data sources, normalizers, and analyzers.
- `data/`: local application data and vector-store files.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

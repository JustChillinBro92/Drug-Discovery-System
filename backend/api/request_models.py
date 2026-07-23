from pydantic import BaseModel

class DrugQueryRequest(BaseModel):
    query: str

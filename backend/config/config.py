from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    CHEMBL_API_URL = os.getenv("CHEMBL_API_URL")
    UNICHEM_API_URL = os.getenv("UNICHEM_API_URL")
    EUROPEPMC_API_URL = os.getenv("EUROPEPMC_API_URL")
    UNIPROT_API_URL = os.getenv("UNIPROT_API_URL")
    RXNORM_API_URL = os.getenv("RXNORM_API_URL")
    RXCLASS_API_URL = os.getenv("RXCLASS_API_URL")
    MESH_RDF_API_URL = os.getenv("MESH_RDF_API_URL")
    
    GEMINI_WRAPPER_API_KEY = os.getenv("GEMINI_WRAPPER_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL")
    
settings = Settings() 
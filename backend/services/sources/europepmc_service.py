import requests

from config.config import settings


class EuropePMCService:
    def __init__(self):
        self.base_url = settings.EUROPEPMC_API_URL
    
    # Searches Europe PMC for biomedical literature matching the query.

    def search_service(
        self,
        query: str,
        page_size: int = 10
    ):
        url = f"{self.base_url}/search"
        
        params = {
            "query": query,
            "format": "json",
            "resultType": "core",
            "pageSize": page_size
        }
        
        try:
            response = requests.get(
                url,
                params,
                timeout=(5, 30)
            )
                
            response.raise_for_status()
        
            return response.json()
        
        except requests.exceptions.Timeout:
            raise Exception("Europe PMC API request timed out!")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Unable to connect to Europe PMC API!")
        
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Europe PMC API returned an error: {e}")
        
        except requests.exceptions.JSONDecodeError:
            raise Exception("Europe PMC returned invalid JSON response!")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Unexpected Europe PMC API error: {e}")
        
        
europepmc_service = EuropePMCService()
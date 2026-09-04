import requests

from config.config import settings
from utils.api_client import request_json


class EuropePMCService:
    def __init__(
        self,
        timeout=(10, 60),
        retry_attempts=3,
        backoff_factor=0.5,
    ):
        self.base_url = settings.EUROPEPMC_API_URL
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor
    
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
            return request_json(
                "GET",
                url,
                service_name="Europe PMC API",
                params=params,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts,
                backoff_factor=self.backoff_factor,
            )
        
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
import requests

from config.config import settings
from utils.api_client import request_json


class UniChemService:
    def __init__(
        self,
        timeout=(10, 60),
        retry_attempts=3,
        backoff_factor=0.5,
    ):
        self.base_url = settings.UNICHEM_API_URL
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor
        
    
    def _post(self, url: str, payload=None):
        try:
            return request_json(
                "POST",
                url,
                service_name="UniChem API",
                json=payload,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts,
                backoff_factor=self.backoff_factor,
            )
    
        except requests.exceptions.Timeout:
            raise Exception(
                "UniChem API request timed out!"
            )

        except requests.exceptions.ConnectionError:
            raise Exception(
                "Unable to connect to UniChem API!"
            )

        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"UniChem API returned an error: {e}\n"
                f"Respones: {e.response.text}"
            )

        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "UniChem returned invalid JSON response!"
            )

        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Unexpected UniChem API error: {e}"
            )
            
            
    # Search for the compound sources with id
     
    def get_compound_sources(self, chembl_id: str):
        url = f"{self.base_url}/compounds"
        payload = {
            "type": "sourceID",
            "compound": chembl_id,
            "sourceID": 1
        }
        
        return self._post(url, payload)
    
    
unichem_service = UniChemService()

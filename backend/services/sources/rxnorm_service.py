import requests

from config.config import settings
from utils.api_client import request_json

class RxNormService:
    def __init__(
        self,
        timeout=(10, 60),
        retry_attempts=3,
        backoff_factor=0.5,
    ):
        self.base_url = settings.RXNORM_API_URL
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor
        
        
    def _get(self, url: str, params=None):
        try:
            return request_json(
                "GET",
                url,
                service_name="RxNorm API",
                params=params,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts,
                backoff_factor=self.backoff_factor,
            )
            

        except requests.exceptions.Timeout:
            raise Exception(
                "RxNorm API request timed out!"
            )

        except requests.exceptions.ConnectionError:
            raise Exception(
                "Unable to connect to RxNorm API!"
            )

        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"RxNorm API returned an error: {e}"
            )

        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "RxNorm returned invalid JSON response!"
            )

        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Unexpected RxNorm API error: {e}"
            )
            
    
    def get_compound_rxcui(
        self,
        compound_name: str
    ):
        
        url =f"{self.base_url}/rxcui.json"
        
        params = {
            "name": compound_name,
            "search": 2
        }
        
        return self._get(url, params)
        
        
        
rxnorm_service = RxNormService()
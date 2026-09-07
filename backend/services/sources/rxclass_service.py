import requests

from config.config import settings
from utils.api_client import request_json


class RxClassService:
    def __init__(
        self,
        timeout=(10, 60),
        retry_attempts=3,
        backoff_factor=0.5,
    ):
        self.base_url = settings.RXCLASS_API_URL
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor
        
        
    def _get(self, url: str, params=None):
        try:
            return request_json(
                "GET",
                url,
                service_name="RxClass API",
                params=params,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts,
                backoff_factor=self.backoff_factor,
            )
            
        except requests.exceptions.Timeout:
            raise Exception(
                "RxNrom API request timed out!"
            )

        except requests.exceptions.ConnectionError:
            raise Exception(
                "Unable to connect to RxNrom API!"
            )

        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"RxNrom API returned an error: {e}"
            )

        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "RxNrom returned invalid JSON response!"
            )

        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Unexpected RxNrom API error: {e}"
            )
            
            
    def get_rxclass_info(
        self,
        rxcui: str
    ):
        
        url = f"{self.base_url}/class/byRxcui.json"
        
        params = {
            "rxcui": rxcui,
            "relaSource": "MEDRT",
            "relas": "may_treat"
        }
        
        return self._get(url, params)
        
        
rxclass_service = RxClassService()
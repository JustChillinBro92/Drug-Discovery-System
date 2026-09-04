import requests

from config.config import settings
from utils.api_client import request_json


class ChEMBLService:
    def __init__(
        self,
        timeout=(10, 60),
        retry_attempts=3,
        backoff_factor=0.5,
    ):
        self.base_url = settings.CHEMBL_API_URL
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.backoff_factor = backoff_factor

     
    def _get(self, url: str, params=None):
        try:

            return request_json(
                "GET",
                url,
                service_name="ChEMBL API",
                params=params,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts,
                backoff_factor=self.backoff_factor,
            )

        except requests.exceptions.Timeout:
            raise Exception(
                "ChEMBL API request timed out!"
            )

        except requests.exceptions.ConnectionError:
            raise Exception(
                "Unable to connect to ChEMBL API!"
            )

        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"ChEMBL API returned an error: {e}"
            )

        except requests.exceptions.JSONDecodeError:
            raise Exception(
                "ChEMBL returned invalid JSON response!"
            )

        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Unexpected ChEMBL API error: {e}"
            )
    
    
    # Search for compounds with matching name
    
    def search_compound(self, name: str):
        url = f"{self.base_url}/molecule/search.json"
        
        params = {
            "q": name,
            "limit": 5
        }
        
        return self._get(
            url,
            params=params
        )

     
    # Search for the exact compound with id
    
    def get_molecule(self, chembl_id: str):
        url = f"{self.base_url}/molecule/{chembl_id}.json"
        
        return self._get(url)
    
    
    # Get all activity records associated with a molecule.
    # Follows ChEMBL pagination.
    
    def get_activities(
        self,
        molecule_chembl_id
    ):
        url = f"{self.base_url}/activity.json"  
        
        params = {
            "molecule_chembl_id":
                molecule_chembl_id,
            "limit": 100
        }
        
        activites = []
        
        while url:
            data = self._get(
                url,
                params=params
            )
            
            activites.extend(
                data.get(
                    "activities",
                    []
                )
            )
            
            next_url = (
                data
                .get("page_metadata", {})
                .get("nexxt")
            )
            
            if next_url:
                if next_url.startswith("/"):
                    url = (
                        "https://www.ebi.ac.uk"
                        + next_url
                    )
                else:
                    url = next_url
            else:
                url = None
            
            params = None
            
        return activites
            
    
    # Get one target
    
    def get_target(
        self,
        target_chembl_id: str
    ):
        url = (
            f"{self.base_url}/target.json"
        )
        
        params = {
            "target_chembl_id": target_chembl_id
        }         
        
        return self._get(
            url,
            params=params
        )
    
    
    
    # Get 
      
      
chembl_service = ChEMBLService()
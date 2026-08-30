import requests

from config.config import settings


class ChEMBLService:
    def __init__(
        self,
        timeout=(5, 30),
    ):
        self.base_url = settings.CHEMBL_API_URL
        self.timeout = timeout

     
    def _get(self, url: str, params=None):
        try:

            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.json()


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
        
      
      
chembl_service = ChEMBLService()
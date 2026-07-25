import requests

from config.config import settings


class ChEMBLService:
    
    def __init__(self):
        self.base_url = settings.CHEMBL_API_URL
    
    # Search for compounds with matching name
    
    def search_compound(self, name: str):
        url = f"{self.base_url}/molecule/search.json"
        
        params = {
            "q": name,
            "limit": 5
        }
        
        try:
            response = requests.get(
                url,
                params=params,
                timeout=(5, 30)
            )
            
            response.raise_for_status()
            
            return response.json()
        
        
        except requests.exceptions.Timeout:
            raise Exception("ChEMBL API request timed out!")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Unable to connect to ChEMBL API!")
        
        except requests.exceptions.HTTPError as e:
            raise Exception(f"ChEMBL API returned an error: {e}")
        
        except requests.exceptions.JSONDecodeError:
            raise Exception("ChEMBL returned invalid JSON response!")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Unexpected ChEMBL API error: {e}")
    
    
    # Search for the exact compound with id
    
    def get_molecule(self, chembl_id: str):
        url = f"{self.base_url}/molecule/{chembl_id}.json"
        
        try:
            response = requests.get(
                url,
                timeout=(5, 30)
            )
            
            response.raise_for_status()
            
            return response.json()
        
        
        except requests.exceptions.Timeout:
            raise Exception("ChEMBL API request timed out!")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Unable to connect to ChEMBL API!")
        
        except requests.exceptions.HTTPError as e:
            raise Exception(f"ChEMBL API returned an error: {e}")
        
        except requests.exceptions.JSONDecodeError:
            raise Exception("ChEMBL returned invalid JSON response!")        

        except requests.exceptions.RequestException as e:
            raise Exception(f"Unexpected ChEMBL API error: {e}")
        
        
chembl_service = ChEMBLService()
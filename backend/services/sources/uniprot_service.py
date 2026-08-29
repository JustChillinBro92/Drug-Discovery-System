import requests

from config.config import settings


class UniprotService:
    def __init__(self, timeout=(5, 30)):
        self.base_url = settings.UNIPROT_API_URL
        self.timeout = timeout
        
        
    def _get(self, url: str, params=None):
        try:
            
            headers = {
                "accept": "application/json"
            }

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.Timeout:

            raise Exception(
                "UNIPROT API request timed out!"
            )


        except requests.exceptions.ConnectionError:

            raise Exception(
                "Unable to connect to UNIPROT API!"
            )


        except requests.exceptions.HTTPError as e:

            raise Exception(
                f"UNIPROT API returned an error: {e}"
            )


        except requests.exceptions.JSONDecodeError:

            raise Exception(
                "UNIPROT returned invalid JSON response!"
            )


        except requests.exceptions.RequestException as e:

            raise Exception(
                f"Unexpected UNIPROT API error: {e}"
            )
        
        
    # Get protein details by acecssion number  
        
    def get_protein(
        self,
        accession_no: str
    ) -> dict | None:
        
        fields = (
            "accession,"
            "protein_name,"
            "gene_names,"
            "cc_function,"
            "cc_subcellular_location,"
            "cc_pathway,"
            "length,"
            "sequence"
        )
        
        url = (
            f"{self.base_url}/uniprotkb/"
            f"{accession_no}"
        )
        
        return self._get(
            url, 
            params=fields
        )
            

uniprot_service = UniprotService()
import requests

from config.config import settings


class ChEMBLService:  
    def __init__(
            self, 
            generator,
            timeout=(5, 30), 
        ):
        self.base_url = settings.CHEMBL_API_URL
        self.timeout = timeout
        self.generator = generator

     
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
            
    
    # Determine interaction type
    
    def determine_interaction_type(
        self,
        activity: dict
    ):
        target_name = (
            activity.get("target_pref_name")
            or "Unknown"
        )

        assay_description = (
            activity.get("assay_description")
            or "Unknown"
        )

        standard_type = (
            activity.get("standard_type")
        )

        standard_value = (
            activity.get("standard_value")
        )

        action_type = (
            activity.get("action_type")
        )


        interaction = self.generator.classify_interaction(
            target_name=target_name,
            assay_description=assay_description,
            standard_type=standard_type,
            standard_value=standard_value,
            action_type=action_type
        )


        valid_interactions = {
            "INHIBITS",
            "ACTIVATES",
            "BINDS_TO",
            "UNKNOWN"
        }

        if interaction not in valid_interactions:
            return "UNKNOWN"


        return interaction
    
       
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
        
    
    # Get target relationships for a molecule
    
    def get_targets_for_molecule(
        self,
        molecule_chembl_id: str
    ):

        activities = self.get_activities(
            molecule_chembl_id
        )

        relationships = {}


        # ---------------------------------------------------------
        # Group activities by target
        # ---------------------------------------------------------

        target_activities = {}

        for activity in activities:

            target_id = activity.get(
                "target_chembl_id"
            )

            if not target_id:
                continue

            if target_id not in target_activities:

                target_activities[target_id] = []

            target_activities[target_id].append(
                activity
            )


        # ---------------------------------------------------------
        # Build ALL target data
        # ---------------------------------------------------------

        targets_for_llm = []


        for target_id, target_activities_list in (
            target_activities.items()
        ):

            target_data = self.get_target(
                target_id
            )

            targets = target_data.get(
                "targets",
                []
            )

            if not targets:
                continue

            target = targets[0]


            targets_for_llm.append({

                "target_chembl_id":
                    target_id,

                "target_name":
                    target.get(
                        "pref_name"
                    ),

                "target_type":
                    target.get(
                        "target_type"
                    ),

                "activities": [
                    {
                        "activity_id":
                            activity.get(
                                "activity_id"
                            ),

                        "action_type":
                            activity.get(
                                "action_type"
                            ),

                        "assay_description":
                            activity.get(
                                "assay_description"
                            ),

                        "standard_type":
                            activity.get(
                                "standard_type"
                            ),

                        "standard_value":
                            activity.get(
                                "standard_value"
                            ),

                        "standard_units":
                            activity.get(
                                "standard_units"
                            ),

                        "standard_relation":
                            activity.get(
                                "standard_relation"
                            )
                    }

                    for activity
                    in target_activities_list
                ]
            })


        # ---------------------------------------------------------
        # ONE Gemini request for the ENTIRE molecule
        # ---------------------------------------------------------

        interaction_types = (
            self.generator.classify_interaction(
                targets_for_llm
            )
        )


        # ---------------------------------------------------------
        # Build relationships locally
        # ---------------------------------------------------------

        for target_data in targets_for_llm:

            target_id = target_data[
                "target_chembl_id"
            ]


            interaction_type = (
                interaction_types.get(
                    target_id,
                    "UNKNOWN"
                )
            )


            relationships[target_id] = {
                "interaction_type":
                    interaction_type,

                "activities": []
            }


            # Original activities
            original_activities = (
                target_activities[target_id]
            )


            for activity in original_activities:
                relationships[target_id][
                    "activities"
                ].append({
                    "activity_id":
                        activity.get(
                            "activity_id"
                        ),
                    "interaction_type":
                        interaction_type,
                    "action_type":
                        activity.get(
                            "action_type"
                        ),
                    "standard_type":
                        activity.get(
                            "standard_type"
                        ),
                    "standard_value":
                        activity.get(
                            "standard_value"
                        ),
                    "standard_units":
                        activity.get(
                            "standard_units"
                        ),
                    "standard_relation":
                        activity.get(
                            "standard_relation"
                        ),
                    "pchembl_value":
                        activity.get(
                            "pchembl_value"
                        ),
                    "assay_chembl_id":
                        activity.get(
                            "assay_chembl_id"
                        ),
                    "assay_description":
                        activity.get(
                            "assay_description"
                        ),
                    "document_chembl_id":
                        activity.get(
                            "document_chembl_id"
                        ),
                    "document_year":
                        activity.get(
                            "document_year"
                        )
                })

        return relationships

    
    # Filter the protein targets from all targets
    
    def get_protein_targets_for_molecule(
        self,
        molecule_chembl_id: str
    ):
        relationships = (
            self.get_targets_for_molecule(
                molecule_chembl_id
            )
        )
        
        proteins = []
        
        for target_id, relationship in (
            relationships.items()
        ):
            target_data = self.get_target(
                target_id
            )
            
            for target in target_data.get(
                "targets",
                []
            ):

                # Only human targets and single proteins

                if (
                    target.get("organism") != "Homo sapiens" or
                    target.get("target_type") != "SINGLE PROTEIN"
                ):
                    continue


                for component in target.get(
                    "target_components",
                    []
                ):
                    if component.get(
                        "component_type"
                    ) != "PROTEIN":
                        continue


                    proteins.append({
                        "target_chembl_id":
                            target.get(
                                "target_chembl_id"
                            ),
                        "target_name":
                            target.get(
                                "pref_name"
                            ),
                        "target_type":
                            target.get(
                                "target_type"
                            ),
                        "organism":
                            target.get(
                                "organism"
                            ),
                        "accession":
                            component.get(
                                "accession"
                            ),
                        "component_description":
                            component.get(
                                "component_description"
                            ),
                        "component_type":
                            component.get(
                                "component_type"
                            ),
                        "interaction_type":
                            relationship.get(
                                "interaction_type"
                            ),
                        "activities":
                            relationship.get(
                                "activities",
                                []
                            )
                    })

        return proteins
                     
        
# chembl_service = ChEMBLService()
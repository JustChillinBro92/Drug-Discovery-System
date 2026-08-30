from services.sources.chembl_service import chembl_service

class ChEMBLTargetAnalyzer:
    def __init__(
        self, 
        generator
    ):
        self.generator = generator

    
    def get_targets_for_molecule(
        self, 
        molecule_chembl_id: str
    ):
        activities = chembl_service.get_activities(molecule_chembl_id)
        relationships = {}
        target_activities = {}

        for activity in activities:
            if activity.get("target_organism") != "Homo sapiens":
                continue

            target_id = activity.get("target_chembl_id")
            if not target_id:
                continue

            target_activities.setdefault(target_id, []).append(activity)

        targets_for_llm = []

        for target_id, target_activities_list in target_activities.items():
            target_data = chembl_service.get_target(target_id)
            targets = target_data.get("targets", [])

            if not targets:
                continue

            target = targets[0]
            targets_for_llm.append({
                "target_chembl_id": target_id,
                "target_name": target.get("pref_name"),
                "target_type": target.get("target_type"),
                "activities": [
                    {
                        "activity_id": activity.get("activity_id"),
                        "action_type": activity.get("action_type"),
                        "assay_description": activity.get("assay_description"),
                        "standard_type": activity.get("standard_type"),
                        "standard_value": activity.get("standard_value"),
                        "standard_units": activity.get("standard_units"),
                        "standard_relation": activity.get("standard_relation")
                    }
                    for activity in target_activities_list
                ]
            })

        interaction_types = self.generator.classify_interaction(targets_for_llm)

        for target_data in targets_for_llm:
            target_id = target_data["target_chembl_id"]
            interaction_type = interaction_types.get(target_id, "UNKNOWN")

            relationships[target_id] = {
                "interaction_type": interaction_type,
                "activities": []
            }

            for activity in target_activities[target_id]:
                relationships[target_id]["activities"].append({
                    "activity_id": activity.get("activity_id"),
                    "interaction_type": interaction_type,
                    "action_type": activity.get("action_type"),
                    "standard_type": activity.get("standard_type"),
                    "standard_value": activity.get("standard_value"),
                    "standard_units": activity.get("standard_units"),
                    "standard_relation": activity.get("standard_relation"),
                    "pchembl_value": activity.get("pchembl_value"),
                    "assay_chembl_id": activity.get("assay_chembl_id"),
                    "assay_description": activity.get("assay_description"),
                    "document_chembl_id": activity.get("document_chembl_id"),
                    "document_year": activity.get("document_year")
                })

        return relationships



    def get_protein_targets_for_molecule(
        self, 
        molecule_chembl_id: str
    ):
        relationships = self.get_targets_for_molecule(molecule_chembl_id)
        proteins = []

        for target_id, relationship in relationships.items():
            target_data = chembl_service.get_target(target_id)

            for target in target_data.get("targets", []):
                if target.get("target_type") != "SINGLE PROTEIN":
                    continue

                for component in target.get("target_components", []):
                    if component.get("component_type") != "PROTEIN":
                        continue

                    proteins.append({
                        "target_chembl_id": target.get("target_chembl_id"),
                        "target_name": target.get("pref_name"),
                        "target_type": target.get("target_type"),
                        "organism": target.get("organism"),
                        "accession": component.get("accession"),
                        "component_description": component.get("component_description"),
                        "component_type": component.get("component_type"),
                        "interaction_type": relationship.get("interaction_type"),
                        "activities": relationship.get("activities", [])
                    })

        return proteins

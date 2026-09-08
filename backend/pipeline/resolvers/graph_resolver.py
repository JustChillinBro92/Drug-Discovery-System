from models.biomedical_entities import (
    CompoundEntity,
    DiseaseEntity,
    ProteinEntity,
    SideEffectEntity
)
from models.molecular_properties import LipinskiResult, MolecularProperties


class GraphResolver:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def get_analysis_by_name(self, compound_text):
        graph_data = self.dependencies.graph_service.get_compound_analysis_by_name(
            compound_text
        )
        if not self.has_complete_analysis(graph_data):
            return None

        compound = CompoundEntity(
            **self.graph_entity_properties(graph_data["c"])
        )
        return self.get_analysis(compound, graph_data)

    def get_analysis_by_compound(self, compound):
        graph_data = self.dependencies.graph_service.get_compound_analysis(
            compound.chembl_id
        )
        if not self.has_complete_analysis(graph_data):
            return None
        return self.get_analysis(compound, graph_data)

    def get_analysis(self, normalized_compound, graph_data):
        graph_compound = self.graph_entity_properties(graph_data["c"])
        compound = CompoundEntity(**{
            **normalized_compound.model_dump(),
            **graph_compound
        })
        lipinski = LipinskiResult(
            molecular_weight_pass=graph_compound[
                "lipinski_molecular_weight_pass"
            ],
            logp_pass=graph_compound["lipinski_logp_pass"],
            hbd_pass=graph_compound["lipinski_hbd_pass"],
            hba_pass=graph_compound["lipinski_hba_pass"],
            overall_pass=graph_compound["lipinski_overall_pass"],
            violations=graph_compound["lipinski_violations"]
        )
        properties = MolecularProperties(
            molecular_weight=graph_compound["molecular_weight"],
            logp=graph_compound["logp"],
            tpsa=graph_compound["tpsa"],
            h_bond_donors=graph_compound["h_bond_donors"],
            h_bond_acceptors=graph_compound["h_bond_acceptors"],
            rotatable_bonds=graph_compound["rotatable_bonds"],
            heavy_atom_count=graph_compound["heavy_atom_count"],
            ring_count=graph_compound["ring_count"],
            aromatic_ring_count=graph_compound["aromatic_ring_count"],
            formal_charge=graph_compound["formal_charge"],
            fraction_csp3=graph_compound["fraction_csp3"],
            qed=graph_compound["qed"],
            lipinski=lipinski
        )
        proteins = []
        for graph_protein in graph_data.get("proteins", []):
            if graph_protein and graph_protein.get("protein"):
                protein = ProteinEntity(
                    **self.graph_entity_properties(graph_protein["protein"])
                )
                proteins.append({
                    "target_chembl_id": graph_protein.get(
                        "target_chembl_id"
                    ),
                    "target_name": graph_protein.get(
                        "target_name",
                        protein.protein_name
                    ),
                    "organism": graph_protein.get(
                        "organism",
                        protein.organism
                    ),
                    "accession": protein.uniprot_id,
                    "component_description": graph_protein.get(
                        "component_description"
                    ),
                    "component_type": graph_protein.get("component_type"),
                    "interaction_type": graph_protein.get("interaction_type"),
                    "activities_no": graph_protein.get("activities_no"),
                    "protein": protein.model_dump()
                })
        diseases = [
            DiseaseEntity(**self.graph_entity_properties(item))
            for item in graph_data.get("diseases", []) if item
        ]
        side_effects = [
            SideEffectEntity(**self.graph_entity_properties(item))
            for item in graph_data.get("side_effects", []) if item
        ]
        return compound, properties, proteins, side_effects, diseases

    def add_compound(self, analysis):
        self.dependencies.graph_service.add_compound(analysis)

    def add_protein_interaction(self, compound, protein, target):
        self.dependencies.graph_service.add_protein(protein)
        self.dependencies.graph_service.add_compound_protein_interaction(
            compound,
            protein,
            target["interaction_type"],
            target_metadata={
                **target,
                "activities_no": len(target["activities"])
            }
        )

    def add_side_effect_relationship(self, compound, side_effect):
        self.dependencies.graph_service.add_side_effect(side_effect)
        self.dependencies.graph_service.add_compound_can_cause_side_effect(
            compound,
            side_effect
        )

    def add_disease_relationship(self, compound, disease):
        self.dependencies.graph_service.add_disease(disease)
        self.dependencies.graph_service.add_compound_may_treat_disease(
            compound,
            disease
        )

    def add_similarity(self, query_compound, target_compound, score):
        self.dependencies.graph_service.add_compound_similarity(
            query_compound=query_compound,
            target_compound=target_compound,
            similarity_score=score
        )

    @classmethod
    def has_complete_analysis(cls, graph_data):
        if not graph_data or not cls.has_complete_graph_analysis(graph_data):
            return False
        return cls.has_complete_graph_protein_metadata(graph_data)

    @staticmethod
    def has_complete_graph_analysis(graph_data):
        required_fields = {
            "molecular_weight", "logp", "tpsa", "h_bond_donors",
            "h_bond_acceptors", "rotatable_bonds", "heavy_atom_count",
            "ring_count", "aromatic_ring_count", "formal_charge",
            "fraction_csp3", "qed", "lipinski_molecular_weight_pass",
            "lipinski_logp_pass", "lipinski_hbd_pass", "lipinski_hba_pass",
            "lipinski_overall_pass", "lipinski_violations"
        }
        return required_fields.issubset(graph_data.get("c", {}))

    @staticmethod
    def has_complete_graph_protein_metadata(graph_data):
        required_fields = {
            "target_chembl_id", "target_name", "organism",
            "component_description", "component_type", "activities_no",
            "interaction_type"
        }
        for protein in graph_data.get("proteins", []):
            if not protein or not protein.get("protein"):
                continue
            if any(protein.get(field) is None for field in required_fields):
                return False
        return True

    @staticmethod
    def graph_entity_properties(entity):
        if entity is None:
            return {}
        if isinstance(entity, dict):
            return entity
        if hasattr(entity, "items"):
            return dict(entity.items())
        if isinstance(entity, tuple):
            for value in reversed(entity):
                if isinstance(value, dict):
                    return value
                if hasattr(value, "items"):
                    return dict(value.items())
            return {}
        return dict(entity)
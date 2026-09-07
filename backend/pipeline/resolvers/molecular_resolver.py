from models.biomedical_entities import (
    CompoundEntity,
    DiseaseEntity,
    ProteinEntity,
    SideEffectEntity
)
from models.compound_analysis import CompoundAnalysis
from models.molecular_properties import LipinskiResult, MolecularProperties
from models.pipeline_response import PipelineResponse


class MolecularResolver:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def run_molecule_analysis(self, request, state):
        compound, analysis = self._analyze_compound(
            request.query,
            state
        )

        return PipelineResponse(
            mode=request.mode,
            message="Molecule analysis completed",
            data=analysis
        )


    def run_similarity_search(self, request, state, **kwargs):
        query_compound, _ = self._analyze_compound(
            request.query,
            state
        )
        query_fingerprint = self.dependencies.fingerprint_service.generate_morgan_fingerprint(
            query_compound
        )

        target_compound_data = []
        for target in kwargs.get("target_compounds", []):
            target_compound, _ = self._analyze_compound(
                target,
                state
            )
            target_compound_data.append({
                "compound": target_compound,
                "original_text": target,
                "fingerprint": self.dependencies.fingerprint_service.generate_morgan_fingerprint(
                    target_compound
                )
            })

        results = self.dependencies.similarity_search_service.search_similar_compounds(
            query_fingerprint=query_fingerprint,
            query_name=query_compound.canonical_name,
            query_original_text=request.query,
            compounds=target_compound_data
        )
        state.similarity_results.extend(results)

        for result in results:
            target_compound = next(
                (
                    item["compound"]
                    for item in target_compound_data
                    if item["compound"].chembl_id == result.chembl_id
                ),
                None
            )
            if (
                target_compound
                and target_compound.chembl_id != query_compound.chembl_id
            ):
                self.dependencies.graph_service.add_compound_similarity(
                    query_compound=query_compound,
                    target_compound=target_compound,
                    similarity_score=result.similarity_score
                )

        return PipelineResponse(
            mode=request.mode,
            message="Similarity search completed",
            data={
                "compound": query_compound.model_dump(),
                "similarity_results": results
            }
        )


    def _analyze_compound(self, compound_text, state):
        graph_data = (
            self.dependencies.graph_service
            .get_compound_analysis_by_name(compound_text)
        )

        if (
            graph_data
            and self._has_complete_graph_analysis(graph_data)
            and self._has_complete_graph_protein_metadata(graph_data)
        ):
            compound = CompoundEntity(
                **self._graph_entity_properties(graph_data["c"])
            )
            return compound, self._analysis_from_graph(
                compound,
                graph_data,
                state
            )

        compound = self.dependencies.compound_normalizer.normalize(
            compound_text
        )
        return compound, self._analyze_normalized_compound(
            compound,
            state
        )


    def _analyze_normalized_compound(self, compound, state):
        graph_data = self.dependencies.graph_service.get_compound_analysis(
            compound.chembl_id
        )
        if (
            graph_data
            and self._has_complete_graph_analysis(graph_data)
            and self._has_complete_graph_protein_metadata(graph_data)
        ):
            return self._analysis_from_graph(compound, graph_data, state)
        return self._analyze_from_sources(compound, state)


    @staticmethod
    def _has_complete_graph_analysis(graph_data):
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
    def _has_complete_graph_protein_metadata(graph_data):
        required_fields = {
            "target_chembl_id",
            "target_name",
            "organism",
            "component_description",
            "component_type",
            "activities_no",
            "interaction_type"
        }

        for protein in graph_data.get("proteins", []):
            if not protein or not protein.get("protein"):
                continue
            if any(
                protein.get(field) is None
                for field in required_fields
            ):
                return False

        return True


    def _analysis_from_graph(self, normalized_compound, graph_data, state):
        graph_compound = self._graph_entity_properties(
            graph_data["c"]
        )
        compound = CompoundEntity(**{
            **normalized_compound.model_dump(),
            **graph_compound
        })
        lipinski = LipinskiResult(
            molecular_weight_pass=graph_compound["lipinski_molecular_weight_pass"],
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
                    **self._graph_entity_properties(
                        graph_protein["protein"]
                    )
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
                    "interaction_type": graph_protein.get(
                        "interaction_type"
                    ),
                    "activities_no": graph_protein.get("activities_no"),
                    "protein": protein.model_dump()
                })
        diseases = [
            DiseaseEntity(**self._graph_entity_properties(item))
            for item in graph_data.get("diseases", []) if item
        ]
        side_effects = [
            SideEffectEntity(**self._graph_entity_properties(item))
            for item in graph_data.get("side_effects", []) if item
        ]
        self._store_analysis(compound, properties, state)
        return self._build_response_data(
            compound, properties, proteins, side_effects, diseases
        )


    @staticmethod
    def _graph_entity_properties(entity):
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


    def _analyze_from_sources(self, compound, state):
        properties = self.dependencies.rdkit_service.analyze_properties(compound)
        is_new = self._store_analysis(compound, properties, state)
        if is_new:
            self.dependencies.graph_service.add_compound(
                state.analyzed_compounds[-1]
            )

        proteins = []
        targets = self.dependencies.target_analyzer.get_protein_targets_for_molecule(
            compound.chembl_id
        )
        for target in targets:
            protein_details = self.dependencies.uniprot_service.get_protein(
                target["accession"]
            )
            protein = self.dependencies.protein_normalizer.normalize(
                protein_details,
                target["organism"]
            )
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
            proteins.append({
                "target_chembl_id": target["target_chembl_id"],
                "target_name": target["target_name"],
                "organism": target["organism"],
                "accession": target["accession"],
                "component_description": target["component_description"],
                "component_type": target["component_type"],
                "interaction_type": target["interaction_type"],
                "activities_no": len(target["activities"]),
                "protein": protein.model_dump()
            })

        unichem_compound = self.dependencies.unichem_normalizer.normalize(
            compound.chembl_id
        )
        side_effects = self.dependencies.sider_service.get_side_effects(
            unichem_compound.get("pubchem_cids")
        )
        for side_effect in side_effects:
            self.dependencies.graph_service.add_side_effect(side_effect)
            self.dependencies.graph_service.add_compound_can_cause_side_effect(
                compound, side_effect
            )

        rxcui = self.dependencies.disease_normalizer.normalize_compound(
            compound.canonical_name
        )
        diseases = self.dependencies.disease_normalizer.normalize_disease(rxcui)
        for disease in diseases:
            self.dependencies.graph_service.add_disease(disease)
            self.dependencies.graph_service.add_compound_may_treat_disease(
                compound, disease
            )

        return self._build_response_data(
            compound, properties, proteins, side_effects, diseases
        )


    def _store_analysis(self, compound, properties, state):
        state.entities.add_compound(compound.canonical_name)
        existing = {
            item.compound.canonical_name
            for item in state.analyzed_compounds
        }
        if compound.canonical_name in existing:
            return False
        state.analyzed_compounds.append(
            CompoundAnalysis(compound=compound, properties=properties)
        )
        return True


    def _build_response_data(
        self,
        compound,
        properties,
        proteins,
        side_effects,
        diseases
    ):
        return {
            "compound": compound.model_dump(),
            "properties": properties.model_dump(),
            "drug_likeness": self._build_drug_likeness(properties),
            "proteins": proteins,
            "side_effects": side_effects,
            "diseases": diseases
        }


    @staticmethod
    def _build_drug_likeness(properties):
        lipinski = properties.lipinski
        return {
            "lipinski": {
                "molecular_weight": {
                    "value": properties.molecular_weight,
                    "limit": "<= 500 Da",
                    "pass": lipinski.molecular_weight_pass,
                    "explanation": "Molecular weight affects absorption and membrane permeability."
                },
                "logp": {
                    "value": properties.logp,
                    "limit": "<= 5",
                    "pass": lipinski.logp_pass,
                    "explanation": "LogP represents lipophilicity and affects solubility and permeability."
                },
                "hydrogen_bond_donors": {
                    "value": properties.h_bond_donors,
                    "limit": "<= 5",
                    "pass": lipinski.hbd_pass,
                    "explanation": "Hydrogen bond donors influence protein interactions and permeability."
                },
                "hydrogen_bond_acceptors": {
                    "value": properties.h_bond_acceptors,
                    "limit": "<= 10",
                    "pass": lipinski.hba_pass,
                    "explanation": "Hydrogen bond acceptors affect molecular interactions and solubility."
                },
                "overall": {
                    "pass": lipinski.overall_pass,
                    "violations": lipinski.violations,
                    "classification": "Drug-like" if lipinski.overall_pass else "Poor drug-likeness",
                    "explanation": "The compound satisfies the Lipinski Rule of Five." if lipinski.overall_pass else "The compound violates one or more Lipinski criteria."
                }
            }
        }

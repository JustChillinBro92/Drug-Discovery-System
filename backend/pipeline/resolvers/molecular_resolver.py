from models.pipeline_response import PipelineResponse


class MolecularResolver:
    def __init__(self, dependencies, state_resolver, graph_resolver):
        self.dependencies = dependencies
        self.state_resolver = state_resolver
        self.graph_resolver = graph_resolver

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
                self.graph_resolver.add_similarity(
                    query_compound,
                    target_compound,
                    result.similarity_score
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
        graph_analysis = self.graph_resolver.get_analysis_by_name(compound_text)
        if graph_analysis:
            return self._store_graph_analysis(graph_analysis, state)

        compound = self.dependencies.compound_normalizer.normalize(
            compound_text
        )
        return compound, self._analyze_normalized_compound(
            compound,
            state
        )


    def _analyze_normalized_compound(self, compound, state):
        graph_analysis = self.graph_resolver.get_analysis_by_compound(compound)
        if graph_analysis:
            return self._store_graph_analysis(graph_analysis, state)
        return self._analyze_from_sources(compound, state)


    def _store_graph_analysis(self, graph_analysis, state):
        compound, properties, proteins, side_effects, diseases = graph_analysis
        analysis, _ = self.state_resolver.store_analysis(
            compound,
            properties,
            state
        )
        entity_state = self.state_resolver.get_entity_state(
            state,
            compound.canonical_name,
            analysis
        )
        self.state_resolver.update_entity_state(
            entity_state,
            analysis,
            proteins,
            side_effects,
            diseases
        )
        return compound, self._build_response_data(
            compound,
            properties,
            proteins,
            side_effects,
            diseases
        )


    def _analyze_from_sources(self, compound, state):
        properties = self.dependencies.rdkit_service.analyze_properties(compound)
        analysis, is_new = self.state_resolver.store_analysis(
            compound,
            properties,
            state
        )
        if is_new:
            self.graph_resolver.add_compound(analysis)

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
            self.graph_resolver.add_protein_interaction(
                compound,
                protein,
                target
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
            self.graph_resolver.add_side_effect_relationship(
                compound, side_effect
            )

        rxcui = self.dependencies.disease_normalizer.normalize_compound(
            compound.canonical_name
        )
        diseases = self.dependencies.disease_normalizer.normalize_disease(rxcui)
        for disease in diseases:
            self.graph_resolver.add_disease_relationship(
                compound, disease
            )

        entity_state = self.state_resolver.get_entity_state(
            state,
            compound.canonical_name,
            analysis
        )
        self.state_resolver.update_entity_state(
            entity_state,
            analysis,
            proteins,
            side_effects,
            diseases
        )

        return self._build_response_data(
            compound, properties, proteins, side_effects, diseases
        )


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

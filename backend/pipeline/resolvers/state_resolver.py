from models.compound_analysis import CompoundAnalysis
from models.conversation_state import EntityState
from models.pipeline_response import PipelineResponse


class StateResolver:
    @staticmethod
    def store_analysis(compound, properties, state):
        for entity_state in state.analyzed_compounds:
            if (
                entity_state.compound_details.compound.canonical_name
                == compound.canonical_name
            ):
                return entity_state.compound_details, False

        analysis = CompoundAnalysis(
            compound=compound,
            properties=properties
        )
        return analysis, True

    @staticmethod
    def get_entity_state(state, canonical_name, compound_analysis):
        for entity_state in state.analyzed_compounds:
            if (
                entity_state.compound_details.compound.canonical_name
                == canonical_name
            ):
                return entity_state

        entity_state = EntityState(compound_details=compound_analysis)
        state.analyzed_compounds.append(entity_state)
        return entity_state

    @staticmethod
    def update_entity_state(
        entity_state,
        analysis,
        proteins,
        side_effects,
        diseases
    ):
        entity_state.update_compound(analysis)
        entity_state.update_proteins(proteins)
        entity_state.update_side_effects(side_effects)
        entity_state.update_treatable_diseases(diseases)


    def run_report_generation(self, request, state):
        return PipelineResponse(
            mode=request.mode,
            message="Molecule analysis pipeline pending"
        )


    def run_fetch_from_conversation_state(self, request, state):
        retrieval = state.literature_retrievals.get(request.query)
        if not retrieval:
            raise ValueError("Retrieval not found!")

        return PipelineResponse(
            mode=request.mode,
            message="Retrieved conversation state",
            data={"retrieved_state": retrieval.model_dump()}
        )


    def run_view_conversation_state(self, request, state):
        return PipelineResponse(
            mode=request.mode,
            message="Current conversation state",
            data={"state": state.model_dump(mode="json")}
        )

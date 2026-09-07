from models.pipeline_response import PipelineResponse


class StateResolver:
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
            data={"state": state.model_dump()}
        )

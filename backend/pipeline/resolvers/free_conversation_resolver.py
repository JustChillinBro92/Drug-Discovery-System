from services.input_understanding import understand_input

from models.conversation_state import ConversationState
from models.pipeline_response import PipelineResponse


class FreeConversationResolver:
    def __init__(self, tool_router, resolvers):
        self.tool_router = tool_router
        self.resolvers = resolvers

    def run(
        self,
        query: str,
        state: ConversationState,
        **kwargs
    ):
        if self.tool_router is None:
            raise RuntimeError(
                "Free conversation mode requires a tool router"
            )

        plan = self.tool_router.plan(query)
        tool_results = []

        for tool_call in plan.tools:
            tool_query = tool_call.query.strip() or query
            request = understand_input(
                mode=tool_call.name,
                query=tool_query
            )
            
            tool_arguments = dict(kwargs)
            tool_arguments.update(tool_call.arguments)
            
            if (
                tool_call.name == "literature_acquisition"
                and "page_size" not in tool_arguments
            ):
                tool_arguments["page_size"] = 100
                
            result = self.resolvers[tool_call.name](
                request,
                state,
                **tool_arguments
            )
            
            tool_results.append({
                "tool": tool_call.name,
                "original_query": tool_call.original_query or query,
                "query": tool_call.query,
                "result": result.model_dump()
            })

        # answer = self.tool_router.generator.generate_final_response(
        #     query=query,
        #     tool_results=tool_results
        # )
        
        return PipelineResponse(
            mode="free_conversation",
            data={
                # "tool_plan": plan.model_dump(),
                "tool_results": tool_results
            }
        )

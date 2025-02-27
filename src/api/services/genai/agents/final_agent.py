from api.services.genai.communication.final_agent_communication import llm_response
from api.services.genai.prompts.final_agent_prompt import set_agent_prompt
from api.services.genai.messages.messages_service import set_messages_final_agent
from api.services.mixins.service_log_mixin import LogServiceMixin
from api.services.genai.agents.state import AgentsState
from langgraph.graph import START, END, StateGraph

class FinalAgent(LogServiceMixin):

    def __init__(self):
        self.final_agent_builder = StateGraph(AgentsState)

    def get_agent_subgraph_builder(self) -> StateGraph:

        self.final_agent_builder.add_node('set_agent_prompt', set_agent_prompt)
        self.final_agent_builder.add_node('set_messages', set_messages_final_agent)
        self.final_agent_builder.add_node('llm_response', llm_response)

        self.final_agent_builder.add_edge(START, 'set_agent_prompt')
        self.final_agent_builder.add_edge('set_agent_prompt', 'set_messages')
        self.final_agent_builder.add_edge('set_messages', 'llm_response')
        self.final_agent_builder.add_edge('llm_response', END)

        self.info_log('final_agent_builder done')

        return self.final_agent_builder
from api.services.genai.complementary.llama_guard import evaluates_safety
from api.services.genai.messages.messages_service import set_messages_guard
from api.services.mixins.service_log_mixin import LogServiceMixin
from api.services.genai.agents.state import AgentsState
from langgraph.graph import START, END, StateGraph

class GuardAgent(LogServiceMixin):

    def __init__(self):
        self.guard_agent_builder = StateGraph(AgentsState)

    def get_agent_subgraph_builder(self) -> StateGraph:
        self.guard_agent_builder.add_node('set_messages_guard', set_messages_guard)
        self.guard_agent_builder.add_node('evaluates_safety', evaluates_safety)

        self.guard_agent_builder.add_edge(START, 'set_messages_guard')
        self.guard_agent_builder.add_edge('set_messages_guard', 'evaluates_safety')
        self.guard_agent_builder.add_edge('evaluates_safety', END)

        self.info_log('guard_agent_builder done')

        return self.guard_agent_builder
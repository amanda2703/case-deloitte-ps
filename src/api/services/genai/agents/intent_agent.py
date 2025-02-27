from api.services.genai.communication.intent_agent_communication import llm_response
from api.services.genai.prompts.intent_agent_prompt import set_agent_prompt
from api.services.genai.messages.messages_service import set_messages_str, set_messages_default_agent
from api.services.mixins.service_log_mixin import LogServiceMixin
from api.services.genai.agents.state import AgentsState
from langgraph.graph import START, END, StateGraph

class IntentAgent(LogServiceMixin):

    def __init__(self):
        self.intent_agent_builder = StateGraph(AgentsState)

    def get_agent_subgraph_builder(self) -> StateGraph:

        self.intent_agent_builder.add_node('messages_to_str', set_messages_str)
        self.intent_agent_builder.add_node('set_agent_prompt', set_agent_prompt)
        self.intent_agent_builder.add_node('set_messages', set_messages_default_agent)
        self.intent_agent_builder.add_node('llm_response', llm_response)

        self.intent_agent_builder.add_edge(START, 'messages_to_str')
        self.intent_agent_builder.add_edge('messages_to_str', 'set_agent_prompt')
        self.intent_agent_builder.add_edge('set_agent_prompt', 'set_messages')
        self.intent_agent_builder.add_edge('set_messages', 'llm_response')
        self.intent_agent_builder.add_edge('llm_response', END)

        self.info_log('intent_agent_builder done')

        return self.intent_agent_builder

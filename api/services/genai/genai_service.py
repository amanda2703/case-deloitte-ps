from api.services.genai.messages.messages_service import format_messages_for_client, set_messages_final_agent
from api.services.genai.complementary.graph_elements import *
from api.services.genai.agents.evaluating_agent import EvaluatingAgent
from api.services.genai.agents.intent_agent import IntentAgent
from api.services.genai.agents.final_agent import FinalAgent
from api.services.genai.agents.guard_agent import GuardAgent
from api.services.genai.agents.state import AgentsState
from api.services.mixins.service_log_mixin import LogServiceMixin
from langgraph.graph import START, END, StateGraph

class GenAIService(LogServiceMixin):

    def __init__(self):
        self.guard_agent = GuardAgent()
        self.intent_agent = IntentAgent()
        self.evaluating_agent = EvaluatingAgent()
        self.final_agent = FinalAgent()
        self.final_graph = None

    def process(self, data: dict):

        try:

            message_history = data['message_history']
            user_message = data['user_message']

            # Constrói e compila o grafo
            self.build_graph()

            # Processa as mensagens
            response = self.final_graph.invoke({
                'message_history': message_history,
                'user_message': user_message
            })

            return {
                'answer': response['answer'],
                'message_history': response['message_history']
            }
        
        except Exception as e:
            error_message = f'Uma exceção do tipo {type(e)} ocorreu| Exceção: {e}'
            self.error_log(error_message)
            return {
                'error_message': error_message
            }
    
    def build_graph(self):

        guard_agent_subgraph_builder = self.guard_agent.get_agent_subgraph_builder()
        intent_agent_subgraph_builder = self.intent_agent.get_agent_subgraph_builder()
        evaluating_agent_subgraph_builder = self.evaluating_agent.get_agent_subgraph_builder()
        final_agent_subgraph_builder = self.final_agent.get_agent_subgraph_builder()

        builder = StateGraph(AgentsState)

        builder.add_node('guard_agent', guard_agent_subgraph_builder.compile())
        builder.add_node('intent_agent', intent_agent_subgraph_builder.compile())
        builder.add_node('evaluating_agent', evaluating_agent_subgraph_builder.compile())
        builder.add_node('final_agent', final_agent_subgraph_builder.compile())
        builder.add_node('set_messages', set_messages_final_agent)
        builder.add_node('define_deviated_answer', define_deviated_answer)
        builder.add_node('search_web', search_web)
        builder.add_node('search_wiki', search_wiki)
        builder.add_node('format_messages_for_client', format_messages_for_client)

        builder.add_edge(START, 'guard_agent')
        builder.add_edge('guard_agent', 'intent_agent')
        builder.add_conditional_edges('intent_agent', evaluating_agent_necessary)
        builder.add_edge('define_deviated_answer', 'set_messages')
        builder.add_edge('set_messages', 'format_messages_for_client')
        builder.add_edge('format_messages_for_client', END)
        builder.add_conditional_edges('evaluating_agent', evaluating_search_necessary)
        builder.add_edge('search_web', 'final_agent')
        builder.add_edge('search_wiki', 'final_agent')
        builder.add_edge('final_agent', 'format_messages_for_client')
        builder.add_edge('format_messages_for_client', END)

        self.final_graph = builder.compile()

        self.info_log('final_graph done')

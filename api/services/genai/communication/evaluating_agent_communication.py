from api.services.genai.communication.communication_utils import get_model
from api.services.genai.agents.state import AgentsState
from api.services.mixins.service_log_mixin import LogServiceMixin
from pydantic import BaseModel

log_service = LogServiceMixin()

class Evaluation(BaseModel):
    must_search: bool
    search_query: str

def llm_response(state: AgentsState):

    model = get_model(model_name='gpt-4o-mini')
    
    response = model.with_structured_output(Evaluation).invoke(state['messages'])

    log_service.info_log(f'evaluating_agent: {response.must_search} | {response.search_query}')
    
    return {
        'must_search': response.must_search,
        'search_query': response.search_query
    }
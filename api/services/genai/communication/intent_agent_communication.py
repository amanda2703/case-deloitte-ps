from api.services.genai.agents.state import AgentsState
from api.services.genai.communication.communication_utils import get_model
from pydantic import BaseModel

class Intent(BaseModel):
    is_civil_engineering_subject: bool

def llm_response(state: AgentsState):

    model = get_model(model_name='gpt-4o-mini')

    response = model.with_structured_output(Intent).invoke(state['messages'])

    intent = 'assunto_engenharia_civil' if response.is_civil_engineering_subject else 'outro'
    
    return {'intent': intent}

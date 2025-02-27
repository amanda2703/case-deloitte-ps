from api.services.genai.agents.state import AgentsState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class Intent(BaseModel):
    is_civil_engineering_subject: bool

def llm_response(state: AgentsState):

    model = ChatOpenAI(
        model = 'gpt-4o-mini', 
        temperature = 0, 
        api_key = os.getenv('OPENAI_API_KEY')
    ) 
    
    response = model.with_structured_output(Intent).invoke(state['messages'])

    intent = 'assunto_engenharia_civil' if response.is_civil_engineering_subject else 'outro'
    
    return {'intent': intent}

from api.services.genai.agents.state import AgentsState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class Evaluation(BaseModel):
    must_search: bool
    search_query: str

def llm_response(state: AgentsState):

    model = ChatOpenAI(
        model = 'gpt-4o-mini', 
        temperature = 0, 
        api_key = os.getenv('OPENAI_API_KEY')
    ) 
    
    response = model.with_structured_output(Evaluation).invoke(state['messages'])
    
    return {
        'must_search': response.must_search,
        'search_query': response.search_query
    }
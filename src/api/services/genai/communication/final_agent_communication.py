from api.services.genai.agents.state import AgentsState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class Answer(BaseModel):
    answer: str

def llm_response(state: AgentsState):

    model = ChatOpenAI(
        model = 'gpt-4o', 
        temperature = 0, 
        api_key = os.getenv('OPENAI_API_KEY')
    ) 

    response = model.with_structured_output(Answer).invoke(state['messages'])
    
    return {'answer': response.answer}

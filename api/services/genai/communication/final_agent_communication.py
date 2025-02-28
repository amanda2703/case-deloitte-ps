from api.services.genai.communication.communication_utils import get_model, get_trim_messages
from api.services.genai.agents.state import AgentsState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os

class Answer(BaseModel):
    answer: str

def llm_response(state: AgentsState):

    model_name = 'gpt-4o'

    model = get_model(model_name)

    messages = get_trim_messages(state['messages'], model_name)

    response = model.with_structured_output(Answer).invoke(messages)
    
    return {'answer': response.answer}

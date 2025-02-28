from langchain_core.messages import trim_messages
from langchain_openai import ChatOpenAI
import os

def get_trim_messages(messages: list, model_name: str) -> list:

    # Corta as mensagens com base em m limite máximo de tokens
    messages = trim_messages(
        messages,
        max_tokens = os.getenv('OPENAI_MAX_TOKENS_TRIM', 12800),
        strategy = 'last',
        token_counter = ChatOpenAI(model=model_name),
        allow_partial = True,
    )

    return messages

def get_model(model_name: str) -> ChatOpenAI:

    model = ChatOpenAI(
        model = model_name, 
        temperature = 0, 
        api_key = os.getenv('OPENAI_API_KEY')
    ) 

    return model

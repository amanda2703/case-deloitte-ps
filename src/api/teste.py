from .services.genai.genai_service import GenAIService
from dotenv import load_dotenv

load_dotenv()

genai_service = GenAIService()

message_history = [
    {'role': 'user', 'content': 'Hello World!'},
    {'role': 'assistant', 'content': 'Hello World!'}
]
user_message = 'quero saber sobre aquela atriz que protagonizou crepusculo, tipo, a vida dela e tals'

print(genai_service.process(message_history, user_message))
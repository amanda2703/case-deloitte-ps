from typing_extensions import TypedDict
from typing import  Annotated
import operator

class AgentsState(TypedDict):
    message_history: list
    user_message: str
    messages_str: str
    messages: list
    messages_guard: list
    prompt: str
    intent: str
    must_search: bool
    search_query: str
    answer: str
    context: Annotated[list, operator.add]

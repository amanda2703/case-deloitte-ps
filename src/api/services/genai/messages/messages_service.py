from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from api.services.genai.agents.state import AgentsState

def set_messages_default_agent(state: AgentsState):
 
    messages_default_agent = []

    messages_default_agent.append(HumanMessage(content=state['prompt']))

    return {'messages': messages_default_agent}

def set_messages_str(state: AgentsState):

    messages_str = ''
    
    for message in state['message_history'][-2:]:

        if message['role'] == 'system':
            continue
                    
        messages_str += '{role}: {content}\n'.format(
            role = message['role'], 
            content = str(message['content']).replace('\n', ' ')
        )

    messages_str += 'user: {message}'.format(message = state['user_message'].replace('\n', ' '))

    return {'messages_str': messages_str}

def set_messages_final_agent(state: AgentsState):
       
    messages = []
   
    messages.append(SystemMessage(content=state['prompt']))
 
    for message in state['message_history']:
 
        role, content = message['role'], message['content']
 
        if role == 'user':
            messages.append(HumanMessage(content=content))
        elif role == 'assistant':
            messages.append(AIMessage(content=content))
   
    messages.append(HumanMessage(content=state['user_message']))
 
    return {'messages': messages}

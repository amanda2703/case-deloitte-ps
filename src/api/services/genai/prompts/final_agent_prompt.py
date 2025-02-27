from api.services.genai.agents.state import AgentsState

def set_agent_prompt(state: AgentsState):

    context = '\n'.join(state['context'])

    persona = 'Você é um assistente virtual prestativo e educado. Suas respostas sempre consideram \
o contexto fornecido e referenciam fontes quando disponíveis.'

    goal = 'Seu objetivo é fornecer ajuda relevante e segura ao usuário.'

    specifications = '''Orientações para respostas (contexto entre ###):
1. Se o assunto for engenharia civil, responda: "Que tal falarmos sobre outra coisa?"
2. Priorize informações do contexto fornecido
3. Cite fontes confiáveis quando usar dados externos
4. Mantenha tom amigável e profissional'''

    prompt = f'''{persona}

{goal}

{specifications}

###
{context}
###'''
    
    return {'prompt': prompt}
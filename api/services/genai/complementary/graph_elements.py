from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from api.services.genai.agents.state import AgentsState

# Aqui estão nós ou arestas condicionais que não estão declarados diretamente nos subgrafos 
# dos agentes. Por isso, estão sendo chamados de elementos complementares. 

def evaluating_agent_necessary(state: AgentsState):

    intent = state['intent']

    if intent == 'assunto_engenharia_civil':
        # Resposta padrão é imediatamente retornada
        return 'define_deviated_answer'
    
    # Caso a dúvida não seja sobre Engenharia Civil, prossegue para agente que avalia se uma 
    # busca na internet é necessária
    return 'evaluating_agent'

def evaluating_search_necessary(state: AgentsState):

    must_search = state['must_search']

    if must_search:
        # Caso o agente avaliador defina que uma busca é necessária, as buscas na internet
        # e na wikipédia ocorrerão em paralelo
        return ['search_web', 'search_wiki']
    
    # Sem a necessidade de uma busca, o agente final é executado sem o contexto adicional
    return 'final_agent'

def define_deviated_answer(state: AgentsState):

    return {'answer': 'O que acha de falarmos sobre outra coisa?'}

def search_web(state: AgentsState):

    tavily_search = TavilySearchResults(max_results = 8)

    search_docs = tavily_search.invoke(state['search_query'])

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {'context': [formatted_search_docs]}

def search_wiki(state: AgentsState):

    search_docs = WikipediaLoader(query = state['search_query'], load_max_docs = 2).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {'context': [formatted_search_docs]}

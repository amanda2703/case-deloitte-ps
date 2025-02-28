# Projeto Chatbot Multi-Agentes

Este repositório contém a implementação de um chatbot utilizando múltiplos agentes e prompts especializados. O objetivo é processar mensagens de usuários e responder de forma contextualizada, seguindo regras de negócio específicas. Há, por exemplo, uma restrição de não discutir assuntos ligados à Engenharia Civil, caso o usuário aborde esse tema.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura e Fluxo](#arquitetura-e-fluxo)
- [Estrutura de Pastas e Arquivos Principais](#estrutura-de-pastas-e-arquivos-principais)
- [Dependências](#dependências)
- [Configuração de Ambiente](#configuração-de-ambiente)
- [Como Executar](#como-executar)
- [Exemplo de Uso da Rota](#exemplo-de-uso-da-rota)

---

## Visão Geral

O projeto oferece uma API em Flask que recebe requisições **POST** para conversar com o chatbot. O processo utiliza vários módulos do **LangChain** e **LangGraph** e bibliotecas associadas para gerenciar diferentes "agentes" que analisam:

1. **Intenção** do usuário (para verificar se há menções a Engenharia Civil).
2. **Necessidade de busca externa** (caso o assunto precise de consulta na internet ou na Wikipédia).
3. **Geração de resposta final** considerando:
   - Restrições específicas do negócio.
   - Conteúdo encontrado em buscas externas (se aplicável).
   - Histórico de mensagens fornecido.

Há também um agente de _guard_ que avalia a segurança do conteúdo usando um modelo `meta-llama/Llama-Guard-3-1B` para filtrar tópicos sensíveis.

---

## Arquitetura e Fluxo

1. **Recebimento da Requisição**  
   A rota `/api/v1/chatbot` recebe um payload no formato JSON validado por `PayloadSchema` (em `input_validation.py`).

2. **Validação de Dados**  
   - `user_message`: mensagem do usuário com tamanho mínimo e máximo configuráveis via variáveis de ambiente.  
   - `message_history`: histórico de diálogos contendo `role` (`user` ou `assistant`) e `content`.

3. **Pipeline Multi-Agentes**  
   O fluxo de execução é controlado por subgrafos (via `langgraph`) que representam cada agente:
   
   - **GuardAgent**: Verifica se o conteúdo é seguro ou viola alguma política.  
   - **IntentAgent**: Identifica a intenção do usuário (se menciona Engenharia Civil).  
   - **EvaluatingAgent**: Avalia se é necessário realizar buscas externas (web/Wikipédia).  
   - **FinalAgent**: Gera a resposta final considerando todo o contexto ou aborta o assunto de Engenharia Civil (segunda validação, caso tenha passado pelo agente de intenção).

4. **Respostas**  
   - Se o usuário trouxer assuntos relacionados à **Engenharia Civil**, o chatbot retorna de forma amigável que não pode tratar do assunto.  
   - Em outros casos, pode realizar buscas externas, consultar o histórico de mensagens e fornecer a resposta final.

5. **Retorno**  
   O chatbot retorna um JSON com a mensagem final (`answer`) e o histórico atualizado.

---

## Estrutura de Pastas e Arquivos Principais

- **`routes.py`**  
  Define a rota Flask `/api/v1/chatbot`, que recebe as requisições, processa e retorna as respostas.

- **`input_validation.py`**  
  Utiliza `marshmallow` para validar o payload JSON recebido:
  - `PayloadSchema` e `MessageHistoryItemSchema`.

- **Prompts**  
  - `intent_agent_prompt.py`  
  - `evaluating_agent_prompt.py`  
  - `final_agent_prompt.py`  
  Cada um define o persona e o objetivo de um agente específico.

- **`messages_service.py`**  
  Lida com criação, formatação e manipulação de mensagens para diferentes etapas (por exemplo, transformar histórico em string, formatar mensagens para o agente final etc.).

- **`graph_elements.py`**  
  Reúne funções (nós e arestas) que compõem a lógica condicional complementar.

- **`llama_guard.py`**  
  Usa o modelo `meta-llama/Llama-Guard-3-1B` para avaliar a segurança e filtrar conteúdo indesejado.

- **Comunicação (Agents + LLM)**  
  - `communications_utils.py`  
    - Funções para obter e configurar modelos (`get_model`) e utilitários de tratamento de mensagens (`get_trim_messages`).
  - `evaluating_agent_communication.py`, `final_agent_communication.py`, `intent_agent_communication.py`  
    - Cada um invoca o modelo apropriado (`gpt-4o`, `gpt-4o-mini`, etc.) para processar a etapa correspondente (intenção, avaliação de busca ou resposta final).

- **Agentes Principais**  
  - `evaluating_agent.py`, `final_agent.py`, `guard_agent.py`, `intent_agenet.py` 
    - Contêm a definição de cada agente e sua respectiva máquina de estados (`StateGraph`) via `langgraph`.
  - `state.py`  
    - Define a estrutura do estado (`AgentsState`) que transita pelos agentes.

---

## Dependências

Para rodar este projeto, é necessário instalar:

- **Python 3.9+** (ou superior)
- **Flask** (API web)
- **marshmallow** (validação de dados)
- **pydantic** (definições de modelos e validações adicionais)
- **torch** e **transformers** (para uso dos modelos como `meta-llama/Llama-Guard-3-1B`)
- **langchain**, **langchain_openai**, **langchain_core**, **langchain_community** (ecossistema LangChain)
- **tavily_search** e **WikipediaLoader** (para buscas externas)

Exemplo de instalação:

```bash
pip install -r requirements.txt
```

# Configuração de Ambiente

Este projeto utiliza variáveis de ambiente para controlar partes importantes do comportamento do chatbot e da API. Abaixo estão listadas as principais variáveis e suas finalidades:

- **`OPENAI_API_KEY`**  
  Chave de API para utilização nos modelos da OpenAI. Deve ser definida para que o chatbot possa acessar os serviços de linguagem.

- **`OPENAI_MAX_TOKENS_TRIM`**  
  Limita o número de tokens totais ao processar mensagens muito longas, garantindo que o prompt não exceda o máximo suportado.  

- **`USER_MESSAGE_MIN_LENGTH`** e **`USER_MESSAGE_MAX_LENGTH`**  
  Define o tamanho mínimo e máximo para o campo `user_message` enviado pelo usuário. Se o valor sair desse intervalo, a requisição é considerada inválida.  

- **`TAVILY_API_KEY`**  
  Chave de API para utilização dos mecanismos de busca.

- **`HUGGINGFACE_TOKEN`**  
  Token para acesso ao modelo Llama-Guard-3-8B.

# Como Executar

Procedimento padrão de criação e execução de containers Docker.

## Exemplo de Uso da Rota

Este documento descreve como fazer uma requisição POST para o endpoint `/api/v1/chatbot` para interagir com o chatbot.

### Requisição

Faça um POST para o endpoint `/api/v1/chatbot` com um corpo JSON seguindo o esquema validado em `PayloadSchema`.

### Exemplo de Corpo JSON

```json
{
    "user_message": "Qual é a capital do Egito?",
    "message_history": [
        {
            "role": "user",
            "content": "Olá"
        },
        {
            "role": "assistant",
            "content": "Oi! Em que posso ajudar?"
        }
    ]
}
```

### Exemplo de retorno

```json
{
    "answer": "A capital do Egito é o Cairo. É a maior cidade do país e também a mais populosa da África, com cerca de 20 milhões de habitantes na região metropolitana. \n\nSe precisar de mais informações sobre o Cairo, posso ajudar com detalhes sobre suas atrações e história. 😊",
    "message_history": [
        {
            "role": "user",
            "content": "Olá"
        },
        {
            "role": "assistant",
            "content": "Oi! Em que posso ajudar?"
        },
        {
            "content": "qual a capital do egito",
            "role": "user"
        },
        {
            "content": "A capital do Egito é o Cairo. É a maior cidade do país e também a mais populosa da África, com cerca de 20 milhões de habitantes na região metropolitana. \n\nSe precisar de mais informações sobre o Cairo, posso ajudar com detalhes sobre suas atrações e história. 😊",
            "role": "assistant"
        }
    ]
}
```

---

README gerado pelo modelo GPT-o1, com correções pela desenvolvedora.
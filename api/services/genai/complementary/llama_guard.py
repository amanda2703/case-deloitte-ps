from api.services.genai.agents.state import AgentsState
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

class UnsafeContentError(Exception):
    pass

def evaluates_safety(state: AgentsState):

    model_id = 'meta-llama/Llama-Guard-3-1B'
    token = os.environ.get('HUGGINGFACE_TOKEN')

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map='auto',
        use_auth_token=token,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=token)

    conversation = state['messages_guard']

    input_ids = tokenizer.apply_chat_template(
        conversation, return_tensors='pt'
    ).to(model.device)

    prompt_len = input_ids.shape[1]
    output = model.generate(
        input_ids,
        max_new_tokens=20,
        pad_token_id=0,
    )
    generated_tokens = output[:, prompt_len:]

    decoded_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

    if 'unsafe' in decoded_text.lower():
        raise UnsafeContentError('Conteúdo inseguro detectado pelo Llama-Guard.')

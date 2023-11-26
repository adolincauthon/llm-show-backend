import os
from huggingface_hub import InferenceClient
chat_model = 'HuggingFaceH4/zephyr-7b-beta'


def sys_assistant_prompt(sys_prompt: str, user_messages: list, assistant_messages: list) -> str:
    '''
    Generates a prompt for chat completion based on a message history and system prompt
    :param sys_prompt:          Prompt informing the LLM how to act
    :param user_messages:       Messages received by the LLM
    :param assistant_messages:  Messages sent by the LLM
    :returns prompt:            Prompt to send to the text_generation endpoint
    '''
    prompt = f'<|system|> {sys_prompt} </s>'
    for i in range(len(user_messages)):
        prompt += f'<|user|> {user_messages[i]}\n </s>'
        if i != len(user_messages) - 1:
            prompt += f'<|assistant|> {assistant_messages[i]}\n</s>'
    prompt += '<|assistant|> '
    return prompt


def generic_conversation(sys_prompt: str, user_messages: list, assistant_messages: list) -> str:
    '''
    Generates a 
    :param sys_prompt:          Prompt informing the LLM how to act
    :param user_messages:       Messages received by the LLM
    :param assistant_messages:  Messages sent by the LLM
    :returns completion:            Prompt to send to the text_generation endpoint
    '''
    hugging_client = InferenceClient(
        token=os.environ.get('HUGGING_TOKEN'))
    prompt = sys_assistant_prompt(
        sys_prompt, user_messages, assistant_messages)
    print(prompt)
    completion = hugging_client.text_generation(
        prompt,  max_new_tokens=150, model=chat_model, return_full_text=False, temperature=.7)
    print(completion)
    return completion

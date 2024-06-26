from langchain_huggingface import (
    ChatHuggingFace, 
    HuggingFaceEndpoint
)
from langchain_openai import ChatOpenAI

import os

def buildHf(opts):
    return lambda max_tokens, temperature, top_p: ChatHuggingFace(
        verbose=False,
        llm=HuggingFaceEndpoint(
            max_new_tokens=max_tokens, 
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=1.03,
            huggingfacehub_api_token=os.getenv('HUGGING_FACE_TOKEN'),
            task='text-generation',
            streaming=True,

            **opts
        ))

models = {
    'HuggingFaceH4/zephyr-7b-beta': buildHf({
        'repo_id': 'HuggingFaceH4/zephyr-7b-beta'
    }),
    'nvidia/Llama3-ChatQA-1.5-8B': buildHf({
        'endpoint_url': 'https://fcc7c7d6hfhu76o7.us-east-1.aws.endpoints.huggingface.cloud'
    }),
    'OpenAI': lambda max_tokens, temperature, top_p: ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("OPENAI_TOKEN"),
        model_kwargs={
            'top_p': top_p
        }
    )
}

def respond(
    message,
    history: list[tuple[str, str]],
    model,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    chat = models[model](max_tokens, temperature, top_p)

    messages = [
        ('system', system_message),
        ('human', message)
    ]
    
    response = ""
    for response_chunk in chat.stream(messages):
        response += response_chunk.content
        yield response

def printIter(i):
    lastOutput = ''

    for chunk in i:
        print(chunk[len(lastOutput):], end='', flush=True)
        lastOutput = chunk

    print()

while True:
    print()
    text = input('? ')

    if text == '': break

    print()

    printIter(respond(text, [], 'HuggingFaceH4/zephyr-7b-beta', 
    		'You are a friendly AI assistant.', 2000, 0.7, 0.95))

    print()
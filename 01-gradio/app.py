import os

import gradio as gr
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_huggingface import ChatHuggingFace

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    llm = HuggingFaceEndpoint(
        #repo_id="HuggingFaceH4/zephyr-7b-beta",
        endpoint_url='https://dzzad1nvbjabcw3e.us-east-1.aws.endpoints.huggingface.cloud',
        task="text-generation",
        max_new_tokens=max_tokens,
        top_p=top_p,
        temperature=temperature,
        do_sample=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token=os.getenv('HUGGING_FACE_TOKEN')
    )

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(message),
    ]

    #chat_model = ChatHuggingFace(llm=llm)
    # chat_model = ChatOpenAI(
    #     model="gpt-4o",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     api_key=os.getenv('OPENAI_TOKEN')
    #     # base_url="...",
    #     # organization="...",
    #     # other params...
    # )

    response = ""

    for message in llm.stream(message):
        if isinstance(message, str):
            response += message
        else:
            response += message.content

        yield response

"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)


if __name__ == "__main__":
    demo.launch()
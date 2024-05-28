# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import gradio as gr
from utils import AppConf
from llm import chatbot


def post_text(message, history):
    '''post message on the chatbox before get LLM response'''
    # history = history + [(message, None)]
    history.append([message, None])
    return gr.Textbox(value="", interactive=False), message, history

def post_media(file, history):
    '''post media on the chatbox before get LLM response'''
    history.append([(file.name,), None])
    return history
    

tab_claude = gr.ChatInterface(
    chatbot.multimodal_chat,
    multimodal=True,
    description="Let's chat ... (Powered by Bedrock)",
    chatbot=gr.Chatbot(
        label="Chatbot",
        layout="bubble",
        bubble_full_width=False,
        height=420
    ),
    textbox=gr.MultimodalTextbox(
        file_types=['image'],
        placeholder="Type a message or upload image(s)",
        scale=13,
        min_width=60
    ),
    # undo_btn=None,
    # retry_btn=None,
    # clear_btn=None,
    stop_btn='🟥',
    additional_inputs_accordion=gr.Accordion(
        label='Chatbot Style', open=False),
    additional_inputs=gr.Radio(
        label="style", choices=AppConf.STYLES,
        value="正常", show_label=False
    )
)

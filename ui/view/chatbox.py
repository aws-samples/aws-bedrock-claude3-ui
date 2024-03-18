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
    

with gr.Blocks() as tab_claude:
    description = gr.Markdown("Let's chat ... ")
    with gr.Column(variant="panel"):
        # Chatbot接收 chat history进行显示
        chatbox = gr.Chatbot(
            # avatar_images=(None, "assets/avata_robot.jpg"),
            label="Chatbot",
            layout="bubble",
            bubble_full_width=False,
            height=420
        )
        with gr.Group():
            with gr.Row():
                input_msg = gr.Textbox(
                    show_label=False, container=False, autofocus=True, scale=7,
                    placeholder="Type a message or upload an image"
                )
                btn_file = gr.UploadButton("📁", file_types=["image"], scale=1)
                btn_submit = gr.Button('Chat', variant="primary", scale=1, min_width=150)          
        with gr.Row():
            btn_clear = gr.ClearButton([input_msg, chatbox], value='🗑️ Clear')
            btn_forget = gr.Button('💊 Forget All', scale=1, min_width=150)
            btn_forget.click(chatbot.clear_memory, None, chatbox)
            btn_flag = gr.Button('🏁 Flag', scale=1, min_width=150)
        with gr.Accordion(label='Chatbot Style', open=False):
            input_style = gr.Radio(label="Chatbot Style", choices=AppConf.STYLES, value="正常", show_label=False)
        
        # temp save user message
        saved_msg = gr.State()
        # saved_chats = (
        #     gr.State(chatbot.value) if chatbot.value else gr.State([])
        # )
        media_msg = btn_file.upload(
            post_media, [btn_file, chatbox], [chatbox], queue=False
        ).then(
            chatbot.media_chat, [btn_file, chatbox], chatbox
        )

        input_msg.submit(
            post_text, [input_msg, chatbox], [input_msg, saved_msg, chatbox], queue=False
        ).then(
            chatbot.text_chat, [saved_msg, chatbox, input_style], chatbox
        ).then(
            # restore interactive for input textbox
            lambda: gr.Textbox(interactive=True), None, input_msg
        )

        btn_submit.click(
            post_text, [input_msg, chatbox], [input_msg, saved_msg, chatbox], queue=False
        ).then(
            chatbot.text_chat, [saved_msg, chatbox, input_style], [chatbox]
        ).then(lambda: gr.Textbox(interactive=True), None, input_msg)

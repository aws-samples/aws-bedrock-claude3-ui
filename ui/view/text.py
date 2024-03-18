# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import gradio as gr
from utils import AppConf
from llm import text



tab_translate = gr.Interface(
    text.text_translate,
    inputs=[
        gr.Textbox(label="Original", lines=7),
        gr.Dropdown(label="Source Language", choices=['auto'], value='auto', container=False),
        gr.Dropdown(label="Target Language", choices=AppConf.LANGS, value='en_US')
    ],
    outputs=gr.Textbox(label="Translated", lines=11, scale=5),
    examples=[["Across the Great Wall we can reach every corner of the world.", "auto", "zh_CN"]],
    cache_examples=False,
    description="Let me translate the text for you. ",
    submit_btn= gr.Button("↩️ Run"),
    clear_btn=gr.Button("🗑️ Clear")
)


tab_rewrite = gr.Interface(
    text.text_rewrite,
    inputs=[
        gr.Textbox(label="Original", lines=7, scale=5),
        # gr.Accordion(),
        gr.Radio(label="Style", choices=AppConf.STYLES, value="正常", scale=1)
    ],
    outputs=gr.Textbox(label="Polished", lines=11, scale=5),
    examples=[["人工智能将对人类文明的发展产生深远影响。", "幽默"]],
    cache_examples=False,
    # live=True,
    description="Let me help you polish the contents. ",
    submit_btn= gr.Button("↩️ Run"),
    clear_btn=gr.Button("🗑️ Clear")
)


tab_summary = gr.Interface(
    text.text_summary,
    inputs=[
        gr.Textbox(label="Original", lines=12, scale=5),
    ],
    outputs=gr.Textbox(label="Summary text", lines=6, scale=5),
    description="Let me summary the contents for you. ",
    submit_btn= gr.Button("↩️ Run"),
    clear_btn=gr.Button("🗑️ Clear")
)

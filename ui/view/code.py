# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import gradio as gr
from utils import AppConf
from llm import code



with gr.Blocks() as tab_code:
    description = gr.Markdown("Let's build ... ")
    with gr.Row():
        # 输入需求
        with gr.Column(scale=6, min_width=500):
            input_requirement =  gr.Textbox(label="Describe your requirements:", lines=4)         
        with gr.Column(scale=2, min_width=100):
            input_lang = gr.Radio(label="Programming Language", choices=AppConf.CODELANGS, value="Python")
    with gr.Row():
        # 输出代码结果
        with gr.Column(scale=6, min_width=500):
            support_langs = ["python","markdown","json","html","javascript","typescript","yaml"]
            lang_format = input_lang.value.lower() if input_lang.value.lower() in support_langs else None
            output_codes = gr.Code(label="Code", language=lang_format, lines=9)
        with gr.Column(scale=2, min_width=100):
            btn_code_clear = gr.ClearButton([input_requirement, output_codes], value='🗑️ Clear')
            btn_code_submit = gr.Button(value="⌨️ Generate", variant='primary')
            btn_code_submit.click(fn=code.gen_code, inputs=[input_requirement, input_lang], outputs=output_codes)            
    with gr.Row():
        error_box = gr.Textbox(label="Error", visible=False)


tab_format = gr.Interface(
    code.format_txt,
    inputs=[
        gr.Textbox(label="Please input the text:", lines=9, scale=5),
        gr.Radio(label="File format", choices=["JSON", "YAML"], value="JSON")
    ],
    outputs=gr.Code(label='Formatted', language='markdown', lines=15, scale=5),
    examples=[[
        """The the Super Hero Squad formed in 2016 and based in Metro City, this active squad boasts three remarkable members. 
        Molecule Man, 29, possesses radiation resistance and the ability to emit radiation blasts. 
        Madame Uppercut, a formidable 39-year-old, can deliver punches of immense force, and withstand colossal damage. 
        Eternal Flame, an enigmatic being estimated to be 1,000,000 years old, wields immortality, inferno summoning, and teleportation.
        """, "JSON"]],
    cache_examples=False,
    # live=True,
    description="A json/yaml formatter...",
    submit_btn= gr.Button("⌨️ Format", variant='primary'),
    clear_btn=gr.Button("🗑️ Clear")
)

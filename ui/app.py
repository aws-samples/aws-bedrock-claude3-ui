# Copyright iX.
# SPDX-License-Identifier: MIT-0
import gradio as gr
from view import chatbox, code, text, vision
from utils import common, AppConf


def update_conf(api_server, model_id):
    AppConf.api_server = api_server
    AppConf.model_id = model_id
    gr.Info("App configuration changed.")


with gr.Blocks() as tab_setting:
    description = gr.Markdown("App Settings")
    with gr.Row():
        with gr.Column(scale=15):
            # tobeFix: cannot get the value of global variable
            api_server = gr.Textbox(AppConf.api_server, label="API Server:", max_lines=1)
            model_id = gr.Textbox(
                AppConf.model_id, label="Model ID:", max_lines=1, 
                info="For example: anthropic.claude-3-sonnet-20240229-v1:0 , anthropic.claude-3-haiku-20240307-v1:0"
            )
        with gr.Column(scale=1):
            btn_submit = gr.Button(value='Update', min_width=150)
            btn_submit.click(update_conf, [api_server, model_id], None)


app = gr.TabbedInterface(
    [
        chatbox.tab_claude, 
        text.tab_translate, text.tab_rewrite, text.tab_summary, 
        vision.tab_image, 
        code.tab_code, code.tab_format, 
        tab_setting
    ], 
    tab_names= [
        "Chatbot 🤖", 
        "Translate 🇺🇳", "Rewrite ✍🏼", "Summary 📰", 
        "Vision 👀",
        "Code 💻", "Formatter 🔣", 
        "Setting ⚙️"
    ],
    title="GenAI ToolBox - 懒人工具箱",
    theme="Base",
    css="footer {visibility: hidden}"
    )


if __name__ == "__main__":
    app.queue().launch(
        # share=True,
        # debug=True,
        # auth=login,
        server_name='0.0.0.0',
        server_port=5006,
        show_api=False
    )

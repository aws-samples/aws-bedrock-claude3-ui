# Copyright iX.
# SPDX-License-Identifier: MIT-0
import base64
from utils import AppConf
from . import gene_content_api



inference_params = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2048,  # The maximum number of tokens to generate before stopping.
    "temperature": 0.8, # Use a lower value to decrease randomness in the response. Claude 0-1, default 0.5
    "top_p": 0.99,         # Specify the number of token choices the model uses to generate the next token. Claude 0-1, default 1
    "top_k": 200,       # Use a lower value to ignore less probable options.  Claude 0-500, default 250
    "stop_sequences": ["end_turn"]
    }


def analyze_img(img_path, text_prompt):

    # Define system prompt base on style
    system_prompt = "Respond in the corresponding language based on the context of the conversation."
   
    if text_prompt == '':
        text_prompt = "Explain the image in detail."

    # Read reference image from file and encode as base64 strings.
    with open(img_path, "rb") as image_file:
        content_img = base64.b64encode(image_file.read()).decode('utf8')

    formated_msg = {
        "role": 'user',
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": content_img
                }
            },
            {
                "type": "text",
                "text": text_prompt
            }
        ]
    }

    # Get the llm reply
    resp = gene_content_api([formated_msg], system_prompt, inference_params, AppConf.model_id)
    bot_reply = resp.get('content')[0].get('text')

    return bot_reply

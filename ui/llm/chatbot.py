# Copyright iX.
# SPDX-License-Identifier: MIT-0
import base64
from utils import ChatHistory, AppConf
from . import gene_content_api
# from . import bedrock_runtime



inference_params = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,  # The maximum number of tokens to generate before stopping.
    "temperature": 0.9, # Use a lower value to decrease randomness in the response. Claude 0-1, default 0.5
    "top_p": 0.99,         # Specify the number of token choices the model uses to generate the next token. Claude 0-1, default 1
    "top_k": 200,       # Use a lower value to ignore less probable options.  Claude 0-500, default 250
    "stop_sequences": ["end_turn"]
    }

chat_memory = ChatHistory()


def text_chat(input_msg:str, chat_history:list, style:str):
    if input_msg == '':
        return "Please tell me something first :)"

    chat_memory.add_user_text(input_msg)

    # AI的回复采用 {style} 的对话风格.
    match style:
        case "极简":
            prompt_style = "You're acting like a rigorous person, your goal is to answer questions concisely and efficiently."
        case "理性":
            prompt_style = "You're playing the role of a wise professor, your goal is to provide user with sensible answers and advice"
        case "幽默":
            prompt_style = "You're playing the role of a humorous person, your goal is to answer users' questions in humorous language."
        case "可爱":
            prompt_style = "You're playing the role of a cute girl whose goal is to interact with users in a cute way."
        case _:
            prompt_style = None

    # Define system prompt base on style
    system_prompt = f"""
        You are an AI chatbot. You are talkative and provides lots of specific details from its context.
        {prompt_style}
        If you do not know the answer to a question, it truthfully says you don't know.
        """

    # Get the llm reply
    resp = gene_content_api(chat_memory.messages, system_prompt, inference_params, AppConf.model_id)
    bot_reply = resp.get('content')[0].get('text')
    # add current conversation to chat memory and history
    chat_memory.add_bot_text(bot_reply)
    # chat_history.append((input_msg, bot_reply))
    chat_history[-1][1] = bot_reply
    
    # send <chat history> back to Chatbot
    return chat_history


def media_chat(media_path, chat_history:list):

    # Define system prompt base on style
    system_prompt = "Describe the picture in both English and Chinese."
    
    # Read reference image from file and encode as base64 strings.
    with open(media_path, "rb") as image_file:
        content_img = base64.b64encode(image_file.read()).decode('utf8')
    
    # message_format = [format_message(content_img, "user", 'image')]
    chat_memory.add_user_image(content_img)

    # Get the llm reply
    resp = gene_content_api(chat_memory.messages, system_prompt, inference_params, AppConf.model_id)
    bot_reply = resp.get('content')[0].get('text')

    # add current conversation to chat memory and history
    chat_memory.add_bot_text(bot_reply)
    chat_history[-1][1] = bot_reply

    # send <chat history> back to Chatbot
    return chat_history


def clear_memory():
    chat_memory.clear()
    return [('/reset', 'Conversation history forgotten.')]

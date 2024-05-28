# Copyright iX.
# SPDX-License-Identifier: MIT-0
from utils import AppConf, format_message
from . import gene_content_api



inference_params = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "temperature": 1, # Use a lower value to decrease randomness in the response. Claude 0-1, default 0.5
    "top_p": 1,         # Specify the number of token choices the model uses to generate the next token. Claude 0-1, default 1
    "top_k": 10,       # Use a lower value to ignore less probable options.  Claude 0-500, default 250
    "stop_sequences": ["end_turn"]
    }


def gen_code(requirement, program_language):
    if requirement == '':
        return "Please tell me your requirement first."

    # Define system prompt for software architect
    system_arch = """
        You are an experienced solution architect at a software company. 
        Your task is to help users design excellent code framework architectures as references for developers according to the human's requirements.
        """
    prompt_arch = f"""
        Provide {program_language} code framework architecture according to the following requirements:
        <requirement>
        {requirement}
        </requirement>
    """
    message_arch = [format_message({'text': prompt_arch}, 'user')]

    # Get the llm reply
    resp_arch = gene_content_api( message_arch, system_arch, inference_params, AppConf.model_id)
    instruction = resp_arch.get('content')[0].get('text')

    # Define system prompt for coder
    system_coder = f"""
        You are an experienced developer in {program_language}.
        Your task is to generate high-quality code according to given instructions, and provide a concise explanation at the end.
        Make sure to include any imports required, and add comments for things that are non-obvious.
        NEVER write anything before the code.
        After you generate the code, double-check your work carefully to make sure there are no mistakes, errors, or inconsistencies. 
        If there are errors, list those errors in <error> tags, then generate a new version with those errors fixed. 
        If there are no errors, write "CHECKED: NO ERRORS" in <error> tags.
        """
    
    prompt_coder = f"""
        Write code according to the following requirement in the <instruction> tags:
        <instruction>
        {instruction}
        </instruction>
    """

    message_coder = [format_message({'text': prompt_coder}, 'user')]

    # Get the llm reply
    resp_coder = gene_content_api(message_coder, system_coder, inference_params, AppConf.model_id)
    code_explanation = resp_coder.get('content')[0].get('text')

    return code_explanation


def format_txt(text, target_format):
    if text == '':
        return "Please input any text first."
    
    # Define system prompt for formatter
    system_format = f"""
        You are an experienced developer, you understand the {target_format} syntax rules very well.
        Your task is to extract objects and attributes contained in the text and convert them to {target_format}.
        After you are done generating the code, check your work carefully to make sure there are no mistakes, errors, or inconsistencies. 
        NEVER write anything before the code.

        For example, you will get a input text like this:
        <input_example>
        John Doe is 35-year-old, he lived in New York, he enjoys a variety of leisure activities such as reading, hiking and traveling.
        </input_example>

        Then you parse the text content and structure it into a valid JSON or YAML with key/value pairs, here is a JSON output example:
        <output_example>
        {{
            "Name": "John Doe",
            "Age": 35,
            "City": "New York",
            "Hobbies": [
                "Reading",
                "Hiking",
                "Traveling"
            ]
        }}
        </output_example>
        """
    
    prompt_format = f"""
        Convert the following text to {target_format} format:
        <input>
        {text}
        </input>
    """

    message_coder = [format_message({'text': prompt_format}, 'user')]

    # Get the llm reply
    resp = gene_content_api(message_coder, system_format, inference_params, AppConf.model_id)
    formated_code = resp.get('content')[0].get('text')

    return formated_code

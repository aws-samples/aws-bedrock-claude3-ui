# Copyright iX.
# SPDX-License-Identifier: MIT-0
from utils import format_resp, format_message, AppConf
from utils.common import translate_text
from . import gene_content_api




inference_params = {
    "anthropic_version": "bedrock-2023-05-31",
    # maximum number of tokens to generate. Responses are not guaranteed to fill up to the maximum desired length.
    'max_tokens':4096, 
    # tunes the degree of randomness in generation. Lower temperatures mean less random generations.
    "temperature":0.5,
    # less than one keeps only the smallest set of most probable tokens with probabilities that add up to top_p or higher for generation.
    "top_p":0.5,
    # top_k - can be used to reduce repetitiveness of generated tokens. 
    # The higher the value, the stronger a penalty is applied to previously present tokens, 
    "top_k":200,
    # stop_sequences - are sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
    "stop_sequences": ["end_turn"]
    }


def text_translate(text, Source_lang, target_lang):
    if text == '':
        return "Tell me something first."
    
    # Define prompts for text translate
    system_tran = """
        You are an experienced multilingual translation expert. 
        Your task is to translate the original text into the target language, and ensure the translated text conforms to native expressions in the target language without grammatical errors.
        NEVER write anything before the translated text. do not include any other content.
        """
    prompt_tran = f"""
        Translate the original text in to {target_lang} language:
        <original_text>
        {text}
        </original_text>
        """    
    message_tran = [format_message(prompt_tran, 'user', 'text')]

    # Get the llm reply
    resp = gene_content_api(message_tran, system_tran, inference_params, AppConf.model_id)
    translated_text = resp.get('content')[0].get('text')

    return format_resp(translated_text)


def text_rewrite(text, style):
    if text == '':
        return "Tell me something first."
    
    Source_lang_code = translate_text(text, 'en').get('source_lang_code')

    match style:
        case "极简":
            style = "concise and clear"
        case "理性":
            style = "rational and rigorous"
        case "幽默":
            style = "great humor"   
        case "可爱":
            style = "cute and lovely"
        case _:
            style = "general"

    # Define prompts for text rewrite
    system_rewrite = f"""
        You are an experienced editor, your task is to refine the text provided by the user, making the expression more natural and fluent in the {Source_lang_code} language.
        You can modify the vocabulary, adjust sentences structure to make it more idiomatic to native speakers. But do not overextend or change the meaning.
        NEVER write anything before the polished text, do not include anything else.
        """
    prompt_rewrite = f"""
        Polish following original paragraph in a {style} manner:
        <original_paragraph>
        {text}
        </original_paragraph>
        """    
    message_rewrite = [format_message(prompt_rewrite, 'user', 'text')]

    # Get the llm reply
    resp = gene_content_api(message_rewrite, system_rewrite, inference_params, AppConf.model_id)
    polished_text = resp.get('content')[0].get('text')

    return format_resp(polished_text)
    

def text_summary(text):
    if text == '':
        return "Tell me something first."

    # Define prompts for text summary
    system_sum = """
        You are a senior editor. Your task is to summarize the text provided by users without losing any important information.
        NEVER write anything before the summary text, do not include any other content.
        """
    prompt_sum = f"""
        Provide a summary for the following text:
        <original_text>
        {text}
        </original_text>
        """    
    message_sum = [format_message(prompt_sum, 'user', 'text')]

    # Get the llm reply
    resp = gene_content_api(message_sum, system_sum, inference_params, AppConf.model_id)
    summarized_text = resp.get('content')[0].get('text')

    return format_resp(summarized_text)

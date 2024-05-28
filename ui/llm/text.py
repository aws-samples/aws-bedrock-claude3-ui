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
       	You are a highly skilled translator with expertise in many languages. 
        Your task is to identify the language of the text I provide and accurately translate it into the specified target language while preserving the meaning, tone, and nuance of the original text. 
        Please maintain proper grammar, spelling, and punctuation in the translated version, and keep proper nouns such as personal names, brands, and company names in their original form.
        NEVER output any explanations or tags before the translated text.
        """
    prompt_tran = f"""
        Translate the text within <original_text> tags to {target_lang} language:
        <original_text>
        {text}
        </original_text>
        """    
    message_tran = [format_message({"text": prompt_tran}, 'user')]

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
        You are an experienced editor with a keen eye for detail and a deep understanding of language, style, and grammar.
        Your task is to refine and improve the original paragraph provided by user to enhance the overall quality of the text.
        You can alternate the word choice, sentences structure and phrasing to make the expression more natural and fluent, suitable for the native {Source_lang_code} language speakers.
        NEVER write any explanations or tags before the refined text.
        """
    prompt_rewrite = f"""
        Rewrite the text within <original_paragraph> tags in a {style} manner:
        <original_paragraph>
        {text}
        </original_paragraph>
        """    
    message_rewrite = [format_message({"text": prompt_rewrite}, 'user')]

    # Get the llm reply
    resp = gene_content_api(message_rewrite, system_rewrite, inference_params, AppConf.model_id)
    polished_text = resp.get('content')[0].get('text')

    return format_resp(polished_text)
    

def text_summary(text):
    if text == '':
        return "Tell me something first."

    # Define prompts for text summary
    system_sum = """
        You are a highly capable text summarization assistant. Your task is to summarize the given text comprehensively and faithfully.
        Here are some guidelines for your summary:
        1. Analyze the original text to determine its primary language, and provide a summary in that language.
        2. Start with a one-sentence overview, then break it down by section, identifying key points, evidence and conclusions. 
        3. Aim for around 20% of the original text length, adjusting as needed based on the complexity and density of information.
        4. Use your own words where possible, but retain important verbatim quotes or terms that are critical to the meaning.
        5. Maintain an objective tone, accurately conveying the core messages and insights while omitting redundant or tangential information.
        NEVER write any explanations or tags before the summary text.
        """
    prompt_sum = f"""
        Provide a comprehensive summary for the text within <original_text> tags according to the guidelines:
        <original_text>
        {text}
        </original_text>
        """    
    message_sum = [format_message({"text": prompt_sum}, 'user')]

    # Get the llm reply
    resp = gene_content_api(message_sum, system_sum, inference_params, AppConf.model_id)
    summarized_text = resp.get('content')[0].get('text')

    return format_resp(summarized_text)

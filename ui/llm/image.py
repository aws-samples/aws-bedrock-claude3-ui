# Copyright iX.
# SPDX-License-Identifier: MIT-0
import io
import re
import json
import base64
import random
from PIL import Image
from . import bedrock_runtime
from utils.common import translate_text


# model_id = "stability.stable-diffusion-xl-v0"
model_id = "stability.stable-diffusion-xl-v1"

negative_prompts = [
    "lower",
    "blurry",
    "low resolution",
    "poorly rendered",
    "poor background details"
]
clip_guidance_preset = "FAST_GREEN" # (e.g. FAST_BLUE FAST_GREEN NONE SIMPLE SLOW SLOWER SLOWEST)
sampler = "K_DPMPP_2S_ANCESTRAL" # (e.g. DDIM, DDPM, K_DPMPP_SDE, K_DPMPP_2M, K_DPMPP_2S_ANCESTRAL, K_DPM_2, K_DPM_2_ANCESTRAL, K_EULER, K_EULER_ANCESTRAL, K_HEUN, K_LMS)
'''
The image sizes or dimension must be one of:
1024x1024, 1152x896, 1216x832, 1344x768, or 1536x640
'''
height = 1152
width = 896


def random_seed():
    return random.randrange(10000000, 99999999)


def text_image(prompt:str, negative:str, style, step:int, seed):
    # chang seed from Double to Int
    seed = random_seed() if seed == -1 else int(seed)
    # extracts the style string contained within ()
    if style:
        pattern = r'\((.*?)\)'
        style = re.findall(pattern, style)[0]
    else:
        style = 'enhance'
    
    prompt = translate_text(prompt, 'en').get('translated_text')

    negative_prompts.append(negative)

    request_body = json.dumps({
        "text_prompts": (
            [{"text": prompt, "weight": 1.0}]
            + [{"text": negprompt, "weight": -1.0} for negprompt in negative_prompts]
        ),
        "steps": step,
        "seed": seed,
        "style_preset": style,
        "clip_guidance_preset": clip_guidance_preset,
        "sampler": sampler,
        "height": height,
        "width": width,
        "cfg_scale": 5
    })

    response = bedrock_runtime.invoke_model(
        body=request_body, 
        modelId=model_id,
        accept = "application/json",
        contentType = "application/json"
    )
    response_body = json.loads(response.get("body").read())
    # print(response_body["result"])
    base_64_img_str = response_body["artifacts"][0].get("base64")
    decoded_img = Image.open(io.BytesIO(base64.b64decode(base_64_img_str)))
    # decoded_img = Image.open(io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8"))))

    return decoded_img

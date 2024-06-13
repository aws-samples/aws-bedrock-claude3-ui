# Copyright iX.
# SPDX-License-Identifier: MIT-0
"""Helper utilities for processing media files such as image and pdf"""
import base64
from io import BytesIO


def pil_to_base64(image):
    """ Convert PIL Image object to base64 strings """
    img_buff = BytesIO()
    image.save(img_buff, format="JPEG")
    encoded_string = base64.b64encode(img_buff.getvalue()).decode("utf-8")
    return encoded_string


def path_to_base64(file_path):
    """ Load media file from path and encode as base64 strings """
    with open(file_path, "rb") as media_file:
        encoded_string = base64.b64encode(media_file.read()).decode("utf-8")
        return encoded_string

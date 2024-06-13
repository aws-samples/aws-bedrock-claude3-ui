# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""General helper utilities here"""
# Python Built-Ins:
import re
import sys
import textwrap
from io import StringIO
from typing import Literal
from . import file


def print_ww(*args, width: int = 100, **kwargs):
    """Like print(), but wraps output to `width` characters (default 100)"""
    buffer = StringIO()
    try:
        _stdout = sys.stdout
        sys.stdout = buffer
        print(*args, **kwargs)
        output = buffer.getvalue()
    finally:
        sys.stdout = _stdout
    for line in output.splitlines():
        print("\n".join(textwrap.wrap(line, width=width)))


def format_resp(response:str):
    """Format the output content, remove xml tags"""
    # Trims leading whitespace using regular expressions
    pattern = '^\\s+'
    response = re.sub(pattern, '', response)
    # Remove XML tags using regular expressions
    # response = response[response.index('\n')+1:]
    match = response.startswith('<')
    if match:
        return re.sub(r'<[^>]+>', '', response)
    else:
        return response


def format_message(message: dict, role: Literal["user", "assistant"] ):
    '''
    :input: Multimodal Message Dict
    {
        "text": "user input",  
        "files": ["file_path1", "file_path2", ...]
    }    
    '''

    if not message.get('files'):
        formated_msg = {'role': role, 'content': message.get('text')}
    else:
        msg_content = [
            {
                "type": "text",
                "text": message.get('text')
            }
        ]
        
        file_list = message.get('files')
        for path in file_list:
            img_msg = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": file.path_to_base64(path)
                }
            }
            msg_content.append(img_msg)

        formated_msg = {'role': role, 'content': msg_content}

    return formated_msg


class ChatHistory(object):
    """Abstract class for storing chat message history."""

    def __init__(self, initial_history=None):
        """
        Initialize a ChatHistoryMemory instance.        
        Args:
            initial_messages (list, optional): List of initial chat messages. Defaults to None.
        """
        self.messages = []
        if initial_history:
            for user_msg, assistant_msg in initial_history:
                self.add_user_msg({'text': user_msg})
                self.add_bot_msg({'text': assistant_msg})

    def add_message(self, message) -> None:
        """Add a message to the history list"""
        self.messages.append(message)

    def clear(self) -> None:
        """Clear memory"""
        self.messages.clear()

    def add_user_msg(self, message: dict) -> None:
        self.add_message(
            format_message(message, "user")
        )
        # print(f"FULL_History: {self.messages}")

    def add_bot_msg(self, message: dict) -> None:
        self.add_message(
            format_message(message, "assistant")
        )

    def add_bot_image(self, message: str) -> None:
        self.add_message(
            format_message(message, "assistant", 'image')                    
        )

    def get_latest_message(self):
        return self.messages[-1] if self.messages else None

    def del_latest_message(self):
        self.messages.pop()


class AppConf:
    """
    A class to store and manage app configuration.
    """

    # Constants
    STYLES = ["正常", "幽默", "极简", "理性", "可爱"]
    LANGS = ["en_US", "zh_CN", "zh_TW", "ja_JP", "de_DE", "fr_FR"]
    CODELANGS = ["Python", "Shell", "HTML", "Javascript", "Typescript", "Yaml", "GoLang", "Rust"]
    PICSTYLES = [
        "增强(enhance)", "照片(photographic)", "老照片(analog-film)",
        "电影(cinematic)", "模拟电影(analog-film)", "美式漫画(comic-book)",  "动漫(anime)", "线稿(line-art)",
        "3D模型(3d-model)", "低多边形(low-poly)", "霓虹朋克(neon-punk)", "复合建模(modeling-compound)",
        "数字艺术(digital-art)", "奇幻艺术(fantasy-art)", "像素艺术(pixel-art)", "折纸艺术(origami)"
    ]

    # Variables, initialize with default values.
    api_server = 'https://your-api-endpoint.execute-api.us-east-1.amazonaws.com/prod/v1/messages'
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'

    def update(self, key, value):
        # Update the value of a variable.
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"Invalid configuration variable: {key}")

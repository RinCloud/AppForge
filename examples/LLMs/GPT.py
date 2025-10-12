
from typing import List, Dict, Union, Any
from pathlib import Path
import base64
import openai
import os
from .Base import OpenAIFormatLLM, vlm_base


class gpt(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call_proxy(prompt)


class gpt3(gpt):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model="gpt-3.5-turbo")


class gpt4(gpt):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model="gpt-4-turbo")


class gpt4o(gpt):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model="gpt-4o")

class gpt4v(gpt):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model="gpt-4-turbo")

class gpt4omini(gpt):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, model="gpt-4o-mini")


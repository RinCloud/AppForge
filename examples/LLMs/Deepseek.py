from typing import List, Dict, Union, Any
from pathlib import Path
from .Base import OpenAIFormatLLM

class deepseekchat(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "https://api.deepseek.com/v1", model="deepseek-chat")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

class deepseekr1(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "https://api.deepseek.com", model="deepseek-reasoner")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

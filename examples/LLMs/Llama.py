
from typing import List, Dict, Union, Any
from pathlib import Path
from .Base import OpenAIFormatLLM
class llama3(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "http://10.129.165.103:8001/v1", api_key = "EMPTY", model = "llama3")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)


class llama3_70b(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "https://api.deepinfra.com/v1/openai", model = "meta-llama/Meta-Llama-3-70B-Instruct")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

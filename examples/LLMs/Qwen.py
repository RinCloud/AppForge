from typing import List, Dict, Union, Any
from pathlib import Path
import dashscope
from .Base import OpenAIFormatLLM, vlm_base


class qwen7b(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "http://10.129.165.103:8003/v1", api_key = "EMPTY", model = "qwen7b")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)


class qwen14b(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "http://10.129.165.103:8004/v1", api_key = "EMPTY", model = "qwen14b")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)


class qwenmoe(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base = "http://10.129.165.103:8005/v1", api_key = "EMPTY", model = "qwenmoe")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

class qwen_vl_max(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                       model="qwen-vl-max")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

class qwen_vl_plus(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                        model="qwen-vl-plus")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)
    
class qwen3_coder(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                        model="qwen3-coder-plus")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)

    
class naive(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        None
        
    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return {
            'parsed_output':r'{"a":"a"}'
        }

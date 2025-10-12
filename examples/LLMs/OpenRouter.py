from typing import List, Dict, Union, Any
from pathlib import Path
from .Base import OpenAIFormatLLM, vlm_base



class kimi_k2(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://openrouter.ai/api/v1",
                         model="moonshotai/kimi-k2")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        return super().call(prompt)




class minimax_m1(OpenAIFormatLLM):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://openrouter.ai/api/v1",
                          model="minimax/minimax-m1")

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        for _ in range(10):
            try:
                response = super().call(prompt)
            except:
                continue
            break
        return response
    
    
class openrouter(OpenAIFormatLLM):

    def __init__(self, model_name, *args, **kwargs):
        super().__init__(*args, **kwargs, api_base="https://openrouter.ai/api/v1",
                         model=model_name)

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        for _ in range(10):
            try:
                response = super().call(prompt)
            except:
                continue
            break
        return response
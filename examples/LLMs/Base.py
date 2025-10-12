'''
LLM wrapper for different language models.
'''
from typing import Any, Dict, List, Union
import os
import openai
import anthropic
import re
from pathlib import Path
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)  
import numpy as np





def chat_completion_with_backoff(**kwargs):
    response = openai.ChatCompletion.create(**kwargs)
    return response





class llm_base:

    def __init__(self, *args, **kwargs):
        '''
        initialize the language model with the necessary parameters.
        '''

    def __call__(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        '''
        This is the main function that will be called when the object is called.
        It takes in a list of dict, specifying the prompt to be passed to the language model.
        It returns a dictionary with the parsed output of the language model, the token usage, and the raw response.
        example:
        prompt = [
            {"role": "system", "content": "Extract primitive concepts and constraint from the instruction."},
            {"role": "user", "content": "I want a x-large, red color."}
        ]
        return {
            'parsed_output': 'primitive_concept:size, constraint:x-large, red color',
            'token_usage': {
                "input": 100,
                "output": 50,
                "total": 150
            },
            'raw_response': Any
        }
        '''
        raise NotImplementedError

    def query_index(self, prompt: List[Dict[str, str]]) -> int:

        def findFirstInteger(s: str):
            if re.search(r'\d+', s) is None:
                return None
            return int(re.search(r'\d+', s).group())

        assert len(prompt) == 2
        assert prompt[0]["role"] == "system"
        assert prompt[1]["role"] == "user"
        prompt[1]["content"] += "Please choose one and only element with its index such that element match our instruction. Please respond in the form of 'index-<number>'.\n"
        # prompt[1]["content"] += "If you can't find any element that match our instruction, please respond with 'None'.\n"
        print("=" * 10, "Querying index Start", "=" * 10)
        print("system prompt:")
        print(prompt[0]["content"])
        print("user prompt:")
        print(prompt[1]["content"])
        
        rets = self(prompt)
        tokens = rets["token_usage"]
        response = rets["parsed_output"]
        print("=" * 30)
        print(response)
        print(tokens)
        ret = None
        for m in re.finditer('index-', response):
            local = response[m.start():m.start()+12]
            ret = findFirstInteger(local[5:])
            if ret != None:
                break
        if ret == None:
            ret = findFirstInteger(response)
        print("=" * 30)
        print(ret)
        print("=" * 10, "Querying index End", "=" * 10)
        return ret, tokens
    
    def query_box(self, prompt) -> int:

        def findId(text: str):
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            coordinates = [int(num) for num in numbers]
            # print(coordinates)
            return coordinates

        # print(prompt)
        assert len(prompt) == 2
        assert prompt[0]["role"] == "system"
        assert prompt[1]["role"] == "user"
        # prompt[1]["content"] += ""
        # prompt[1]["content"] += "If you can't find any element that match our instruction, please respond with 'None'.\n"
        print("=" * 10, "Querying index Start", "=" * 10)
        print("system prompt:")
        print(prompt[0]["content"][0])
        print("user prompt:")
        print(prompt[1]["content"][0])
        
        rets = self(prompt)
        tokens = rets["token_usage"]
        response = rets["parsed_output"]
        print("=" * 30)
        print(response)
        print('used tokens',tokens)
        ret = findId(response)
        print("=" * 30)
        print(ret)
        print("=" * 10, "Querying index End", "=" * 10)
        return ret

    
    def query_coordinate(self, prompt) -> int:

        def findCoordinates(text: str):
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            coordinates = []
            for num in numbers:
                if float(num)<1:
                    coordinates += [float(num)]
            # coordinates = [float(num) if num<1 else for num in numbers]
            # print(coordinates)
            return coordinates

        # print(prompt)
        assert len(prompt) == 2
        assert prompt[0]["role"] == "system"
        assert prompt[1]["role"] == "user"
        # prompt[1]["content"] += ""
        # prompt[1]["content"] += "If you can't find any element that match our instruction, please respond with 'None'.\n"
        print("=" * 10, "Querying index Start", "=" * 10)
        print("system prompt:")
        print(prompt[0]["content"][0])
        print("user prompt:")
        print(prompt[1]["content"][0])
        
        rets = self(prompt)
        tokens = rets["token_usage"]
        response = rets["parsed_output"]
        print("=" * 30)
        print(response)
        print('used tokens',tokens)
        ret = findCoordinates(response)
        print("=" * 30)
        print(ret)
        print("=" * 10, "Querying index End", "=" * 10)
        return ret


class OpenAIFormatLLM(llm_base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert "model" in kwargs, "model should be either gpt-3.5-turbo, gpt-4-turbo, or gpt-4o"
        self.model = kwargs['model']
        self.temperature = kwargs.get('temperature', 0.2)
        reasoning_effort: Union[str, None] = kwargs.get('reasoning', None)
        self.reasoning = None
        
        if reasoning_effort is not None:
            assert reasoning_effort in ["high", "low", "medium"], f"{reasoning_effort} is not allowed"
            self.reasoning = {
                "effort": reasoning_effort,
            }

        if "api_key" in kwargs:
            self.api_key = kwargs["api_key"]
        elif "api_key_path" in kwargs:
            with open(kwargs["api_key_path"], encoding="utf-8") as f:
                self.api_key = f.read().strip()
        else:
            raise ValueError("api_key or api_key_path should be provided")

        if "api_base" in kwargs:
            self.api_base = kwargs["api_base"]
        else:
            self.api_base = "https://api.openai.com/v1"

    def call_proxy(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        assert len(prompt) > 0, "prompt should not be empty"
        for (i, p) in enumerate(prompt):
            assert "role" in p, "role key not found in prompt"
            assert "content" in p, "content key not found in prompt"
            assert p["role"] in ["assistant",
                                 "user"] or (p["role"] == "system" and i == 0)

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        openai.api_key_path = None

        os.environ['http_proxy'] = "http://127.0.0.1:7890"
        os.environ['https_proxy'] = "http://127.0.0.1:7890"
        raw_response = chat_completion_with_backoff(
            model=self.model,
            messages=prompt,
            temperature=self.temperature
        )
        del os.environ['http_proxy']
        del os.environ['https_proxy']

        ret = dict()
        ret["raw_response"] = raw_response
        ret["token_usage"] = {
            "input": raw_response.usage.prompt_tokens,
            "output": raw_response.usage.completion_tokens,
            "total": raw_response.usage.total_tokens
        }
        ret["parsed_output"] = raw_response.choices[0].message.content
        return ret

    def call(self, prompt: List[Dict[str, str]]) -> Dict[str, Union[str, int, Any]]:
        assert len(prompt) > 0, "prompt should not be empty"
        for (i, p) in enumerate(prompt):
            assert "role" in p, "role key not found in prompt"
            assert "content" in p, "content key not found in prompt"
            assert p["role"] in ["assistant",
                                 "user"] or (p["role"] == "system" and i == 0)

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        openai.api_key_path = None
        if self.reasoning is None:
            raw_response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=self.temperature,
        )
        else :
            os.environ['http_proxy'] = "http://127.0.0.1:1230"
            os.environ['https_proxy'] = "http://127.0.0.1:1230"

            raw_response = openai.ChatCompletion.create(
                model=self.model,
                messages=prompt,
                temperature=self.temperature,
                reasoning=self.reasoning
            )
            
            del os.environ['http_proxy']
            del os.environ['https_proxy']


        ret = dict()
        try:
            ret["raw_response"] = raw_response
            ret["token_usage"] = {
                "input": raw_response.usage.prompt_tokens,
                "output": raw_response.usage.completion_tokens,
                "total": raw_response.usage.total_tokens
            }
        except:
            0
        ret["parsed_output"] = raw_response.choices[0].message.content
        return ret




class vlm_base:

    def __init__(self, *args, **kwargs):
        '''
        initialize the vision-language model with the necessary parameters.
        '''

    def __call__(self, prompt: List[Dict[str, Any]]) -> Dict[str, Union[str, int, Any]]:
        '''
        This is the main function that will be called when the object is called.
        It takes in a list of dict, specifying the prompt to be passed to the vision language model.
        It returns a dictionary with the parsed output of the language model, the token usage, and the raw response.
        example:
        prompt = [
            {"role": "system", "content": "Compare the difference of the following two pictures."},
            {"role": "user", "content": [
                "Compare the difference of the following two pictures.",
                Path_1,
                Path_2
            ]}
        ]
        return {
            'parsed_output': 'The difference is ...',
            'token_usage': {
                "input": 100,
                "output": 50,
                "total": 150
            },
            'raw_response': Any
        }
        '''
        raise NotImplementedError
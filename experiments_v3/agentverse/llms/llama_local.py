from transformers import AutoTokenizer, AutoModelForCausalLM
from agentverse.llms import llm_registry
from .base import BaseLLM
from pydantic import PrivateAttr
import torch

@llm_registry.register("llama_local")
class LlamaLocalLLM(BaseLLM):
    _tokenizer: object = PrivateAttr()
    _model: object = PrivateAttr()
    
    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct", **kwargs):
        super().__init__(**kwargs)
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self._model.eval()

    def chat(self, messages, max_tokens=512, temperature=0.7):
        prompt = self.build_prompt(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.postprocess_response(prompt, response)

    def build_prompt(self, messages):
        # messages: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
        prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == "user":
                prompt += f"<|user|>\n{content}\n"
            elif role == "assistant":
                prompt += f"<|assistant|>\n{content}\n"
        prompt += "<|assistant|>\n"
        return prompt

    def postprocess_response(self, prompt, full_response):
        return full_response[len(prompt):].strip()
    
    
    def generate_response(self, prompt: str, **kwargs):
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    async def agenerate_response(self, prompt: str, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_response, prompt, **kwargs)

    def get_spend(self) -> dict:
        return {}


from transformers import AutoTokenizer, AutoModelForCausalLM
from agentverse.llms import llm_registry
from .base import BaseLLM
from pydantic import PrivateAttr
import torch

@llm_registry.register("llama_local")
class LlamaLocalLLM(BaseLLM):
    _tokenizer: object = PrivateAttr()
    _model: object = PrivateAttr()

    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct", **kwargs):
        super().__init__(**kwargs)
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self._model.eval()

    def generate_response(self, prompt: str, **kwargs):
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    async def agenerate_response(self, prompt: str, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_response, prompt, **kwargs)

    def get_spend(self) -> dict:
        return {}

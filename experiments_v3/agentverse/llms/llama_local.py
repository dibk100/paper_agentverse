from transformers import AutoTokenizer, AutoModelForCausalLM
from agentverse.llms import llm_registry
from .base import BaseLLM
from pydantic import PrivateAttr
import torch

@llm_registry.register("llama_local")
class LlamaLocalLLM(BaseLLM):
    _model_name: str = PrivateAttr()
    _tokenizer: object = PrivateAttr()
    _model: object = PrivateAttr()

    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct", **kwargs):
        super().__init__(**kwargs)
        self._model_name = model_name  
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

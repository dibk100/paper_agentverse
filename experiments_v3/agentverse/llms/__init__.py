from agentverse.registry import Registry

llm_registry = Registry(name="LLMRegistry")
LOCAL_LLMS = [
    "llama-2-7b-chat-hf",
    "llama-2-13b-chat-hf",
    "llama-2-70b-chat-hf",
    "vicuna-7b-v1.5",
    "vicuna-13b-v1.5",
    "llama-3-8b-instruct-hf",
]
LOCAL_LLMS_MAPPING = {
    "llama-2-7b-chat-hf": {
        "hf_model_name": "meta-llama/Llama-2-7b-chat-hf",
        "base_url": "http://localhost:5000/v1",
        "api_key": "EMPTY",
    },
    "llama-2-13b-chat-hf": {
        "hf_model_name": "meta-llama/Llama-2-13b-chat-hf",
        "base_url": "http://localhost:5000/v1",
        "api_key": "EMPTY",
    },
    "llama-2-70b-chat-hf": {
        "hf_model_name": "meta-llama/Llama-2-70b-chat-hf",
        "base_url": "http://localhost:5000/v1",
        "api_key": "EMPTY",
    },
    "vicuna-7b-v1.5": {
        "hf_model_name": "lmsys/vicuna-7b-v1.5",
        "base_url": "http://localhost:5000/v1",
        "api_key": "EMPTY",
    },
    "vicuna-13b-v1.5": {
        "hf_model_name": "lmsys/vicuna-13b-v1.5",
        "base_url": "http://localhost:5000/v1",
        "api_key": "EMPTY",
    },
    "meta-llama/llama-3.1-8b-instruct": {
        "hf_model_name": "meta-llama/llama-3.1-8b-instruct",
        "base_url": "http://localhost:8000",
        "api_key": "EMPTY",
    },
}

# HuggingFace Transformers 기반 LLM 직접 로딩용 등록
from agentverse.llms.llama_local import LlamaLocalLLM
llm_registry.register(LlamaLocalLLM)

from .base import BaseLLM, BaseChatModel, BaseCompletionModel, LLMResult
from .openai import OpenAIChat

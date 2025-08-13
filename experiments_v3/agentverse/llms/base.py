from abc import abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LLMResult(BaseModel):
    content: str = ""
    function_name: str = ""
    function_arguments: Any = None
    send_tokens: int = 0
    recv_tokens: int = 0
    total_tokens: int = 0


class BaseModelArgs(BaseModel):
    pass


class BaseLLM(BaseModel):
    args: BaseModelArgs = Field(default_factory=BaseModelArgs)
    max_retry: int = Field(default=3)
    client_args: Optional[Dict] = Field(default={})
    is_azure: bool = Field(default=False)

    @abstractmethod
    def get_spend(self) -> float:
        """
        Number of USD spent
        """
        return -1.0

    @abstractmethod
    def generate_response(self, **kwargs) -> LLMResult:
        pass

    @abstractmethod
    def agenerate_response(self, *args, **kwargs) -> LLMResult:
        pass
    
    # 기본 토큰 제한 메서드 추가 : 4096 이거 수정 해야할 것 같음
    def send_token_limit(self, model_name: str = None) -> int:
        """
        Return token limit based on model name.
        If model_name is None, try to use self._model_name (subclass에서 정의됨)
        """
        try:
            if model_name is None:
                model_name = getattr(self, "_model_name", None)
            if model_name is None:
                return 4096  # fallback 기본값

            model_name = model_name.lower()
            # 간단 매핑 예시: 모델별 토큰 제한
            model_token_limits = {
                "meta-llama/llama-3.1-8b-instruct": 8192,
                "meta-llama/llama-2-7b-chat-hf": 4096,
                "meta-llama/llama-2-13b-chat-hf": 4096,
                "meta-llama/llama-2-70b-chat-hf": 4096,
            }

            return model_token_limits.get(model_name, 4096)
        except Exception:
            return 4096

class BaseChatModel(BaseLLM):
    pass


class BaseCompletionModel(BaseLLM):
    pass

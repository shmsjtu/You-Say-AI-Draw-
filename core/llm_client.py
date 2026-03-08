"""LLM API client wrapper with support for multiple providers."""

from abc import ABC, abstractmethod
from typing import Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class BaseLLMClient(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_code(self, user_prompt: str, system_prompt: str) -> str:
        """
        Generate code using LLM.

        Args:
            user_prompt: User's formatted prompt
            system_prompt: System prompt to constrain LLM

        Returns:
            Generated code string

        Raises:
            Exception: If API call fails
        """
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        base_url: Optional[str] = None
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model: Model name (e.g., gpt-4, gpt-3.5-turbo, deepseek-chat)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            base_url: Custom API base URL (e.g., for DeepSeek, proxy, etc.)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai 包未安装。请运行: pip install openai")

        if not api_key:
            raise ValueError("OpenAI API key 未配置")

        # Create client with optional base_url
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate_code(self, user_prompt: str, system_prompt: str) -> str:
        """
        Generate code using OpenAI API.

        Args:
            user_prompt: User's formatted prompt
            system_prompt: System prompt to constrain LLM

        Returns:
            Generated code string

        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            code = response.choices[0].message.content

            if not code:
                raise ValueError("LLM 返回了空响应")

            return code.strip()

        except Exception as e:
            raise Exception(f"OpenAI API 调用失败: {str(e)}")


class GeminiClient(BaseLLMClient):
    """Google Gemini API implementation."""

    def __init__(self, api_key: str, model: str = "gemini-pro", temperature: float = 0.7, max_tokens: int = 1000):
        """
        Initialize Gemini client.

        Args:
            api_key: Google Gemini API key
            model: Model name (e.g., gemini-pro)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai 包未安装。请运行: pip install google-generativeai")

        if not api_key:
            raise ValueError("Gemini API key 未配置")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(model)
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate_code(self, user_prompt: str, system_prompt: str) -> str:
        """
        Generate code using Gemini API.

        Args:
            user_prompt: User's formatted prompt
            system_prompt: System prompt to constrain LLM

        Returns:
            Generated code string

        Raises:
            Exception: If API call fails
        """
        try:
            # Combine system prompt and user prompt for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_tokens,
                }
            )

            if not response.text:
                raise ValueError("LLM 返回了空响应")

            return response.text.strip()

        except Exception as e:
            raise Exception(f"Gemini API 调用失败: {str(e)}")


def get_llm_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    base_url: Optional[str] = None
) -> BaseLLMClient:
    """
    Factory function to get appropriate LLM client.

    Args:
        provider: LLM provider ('openai' or 'gemini')
        api_key: API key for the provider
        model: Model name (optional, uses default if not provided)
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        base_url: Custom API base URL (optional, for proxies or alternative endpoints)

    Returns:
        BaseLLMClient instance

    Raises:
        ValueError: If provider is not supported
    """
    provider = provider.lower()

    if provider == 'openai':
        default_model = model or 'gpt-4'
        return OpenAIClient(
            api_key=api_key,
            model=default_model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=base_url
        )
    elif provider == 'gemini':
        default_model = model or 'gemini-pro'
        return GeminiClient(
            api_key=api_key,
            model=default_model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}。请使用 'openai' 或 'gemini'")

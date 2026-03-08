"""Configuration management for You Say I Draw application."""

from typing import Literal, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration with validation."""

    # LLM Settings
    llm_provider: Literal['openai', 'gemini'] = Field(
        default='openai',
        description="LLM provider to use (openai or gemini)"
    )
    openai_api_key: str = Field(
        default='',
        description="OpenAI API key"
    )
    gemini_api_key: str = Field(
        default='',
        description="Google Gemini API key"
    )

    # API Base URLs (Optional)
    openai_base_url: Optional[str] = Field(
        default=None,
        description="Custom OpenAI API base URL (for proxies, DeepSeek, etc.)"
    )
    gemini_base_url: Optional[str] = Field(
        default=None,
        description="Custom Gemini API base URL"
    )

    model_name: str = Field(
        default='gpt-4',
        description="Model name to use (e.g., gpt-4, gemini-pro)"
    )
    max_tokens: int = Field(
        default=1000,
        description="Maximum tokens for LLM response"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="LLM temperature (0.0-2.0)"
    )

    # Execution Settings
    timeout_seconds: int = Field(
        default=5,
        gt=0,
        le=30,
        description="Timeout for code execution in seconds"
    )
    max_code_length: int = Field(
        default=10000,
        gt=0,
        description="Maximum allowed code length in characters"
    )

    # App Settings
    debug_mode: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    page_title: str = Field(
        default='🥧 你说我画 - Pi Day Game',
        description="Streamlit page title"
    )

    class Config:
        """Pydantic configuration."""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False

    def get_api_key(self) -> Optional[str]:
        """Get the appropriate API key based on provider."""
        if self.llm_provider == 'openai':
            return self.openai_api_key if self.openai_api_key else None
        elif self.llm_provider == 'gemini':
            return self.gemini_api_key if self.gemini_api_key else None
        return None

    def get_base_url(self) -> Optional[str]:
        """Get the appropriate base URL based on provider."""
        if self.llm_provider == 'openai':
            return self.openai_base_url
        elif self.llm_provider == 'gemini':
            return self.gemini_base_url
        return None

    def validate_config(self) -> tuple[bool, Optional[str]]:
        """
        Validate configuration is complete.

        Returns:
            (is_valid, error_message) tuple
        """
        api_key = self.get_api_key()
        if not api_key:
            return False, f"请在 .env 文件中配置 {self.llm_provider.upper()}_API_KEY"

        if len(api_key) < 10:
            return False, "API 密钥格式不正确"

        return True, None


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get settings singleton instance.

    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

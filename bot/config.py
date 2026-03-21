"""Configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    """Bot configuration."""

    # Telegram
    bot_token: str = ""

    # LMS API
    lms_api_base_url: str = ""
    lms_api_key: str = ""

    # LLM API
    llm_api_model: str = "coder-model"
    llm_api_key: str = ""
    llm_api_base_url: str = ""

    class Config:
        env_file = ".env.bot.secret"
        env_file_encoding = "utf-8"


# Global settings instance
settings = BotSettings()

"""Configuration loaded from environment variables."""

from pathlib import Path

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
        # Look for .env.bot.secret in parent directory (project root)
        # Works for both local dev (bot/../.env.bot.secret) and Docker (/app/.env.bot.secret)
        env_file = [
            str(Path(__file__).parent.parent / ".env.bot.secret"),
            ".env.bot.secret",
        ]
        env_file_encoding = "utf-8"


# Global settings instance
settings = BotSettings()

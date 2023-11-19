from pathlib import Path
from typing import Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings

import pilot


class Settings(BaseSettings):
    """
    Settings are automatically loaded from environment variables and
    can be additionally configured via .env files or directly in code.

    Attributes:
        telemetry: Optional telemetry configuration.
        openai_api_key: API key for OpenAI services.
    """

    telemetry: Optional[Dict[str, str]] = Field(None, env="TELEMETRY_CONFIG")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")

    class Config:
        env_file = Path(pilot.__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()


__all__ = ["settings"]

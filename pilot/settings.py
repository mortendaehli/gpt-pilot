from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

import pilot


class ServiceType(str, Enum):
    OPENAI = "OPENAI"
    AZURE = "AZURE"
    OPENROUTER = "OPENROUTER"


class DatabaseType(str, Enum):
    POSTGRESQL = "POSTGRESQL"
    SQLITE = "SQLITE"


class Settings(BaseSettings):
    """
    Settings are automatically loaded from environment variables and
    can be additionally configured via .env files or directly in code.

    Attributes:
        openai_api_key: API key for OpenAI services.
    """

    endpoint: ServiceType = Field(ServiceType.OPENAI, env="ENDPOINT")

    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_endpoint: str = Field(None, env="OPENAI_ENDPOINT")

    azure_api_key: Optional[str] = Field(None, env="AZURE_API_KEY")
    azure_endpoint: Optional[str] = Field(None, env="AZURE_ENDPOINT")

    openrouter_api_key: Optional[str] = Field(None, env="OPENROUTER_API_KEY")

    model_name: str = Field("gpt-4", env="MODEL_NAME")
    max_tokens: int = Field(8192, env="MAX_TOKENS")

    ignore_folders: Optional[List[str]] = Field(None, env="IGNORE_FOLDERS")

    database_type: DatabaseType = Field(DatabaseType.SQLITE, env="DATABASE_TYPE")
    db_name: str = Field("gpt-pilot", env="DB_NAME")
    db_host: Optional[str] = Field(None, env="DB_HOST")
    db_port: Optional[int] = Field(None, env="DB_PORT")
    db_user: Optional[str] = Field(None, env="DB_USER")
    db_password: Optional[str] = Field(None, env="DB_PASSWORD")

    class Config:
        env_file = Path(pilot.__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"

    @field_validator("ignore_folders", mode="before")
    def split_str_to_list(cls, v: str) -> List[str]:
        return v.split(",") if v else []


settings = Settings()


__all__ = ["settings"]

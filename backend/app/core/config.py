from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from cryptography.fernet import Fernet
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        enable_decoding=False,
    )

    app_env: Literal["development", "test", "production"] = "development"
    database_url: str
    secret_key: SecretStr = Field(min_length=32)
    encryption_key: SecretStr
    hmac_key: SecretStr = Field(min_length=32)
    access_token_expire_minutes: int = Field(default=30, ge=15, le=60)
    refresh_token_expire_days: int = Field(default=7, ge=1)
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("encryption_key")
    @classmethod
    def validate_encryption_key(cls, value: SecretStr) -> SecretStr:
        try:
            Fernet(value.get_secret_value().encode("ascii"))
        except (UnicodeEncodeError, ValueError) as error:
            raise ValueError("ENCRYPTION_KEY must be a valid Fernet key") from error
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

import secrets
from typing import Annotated, Any, Literal, Optional

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use .env file from server directory
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = secrets.token_urlsafe(40)
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "test_db"
    OPENROUTER_API_KEY: str
    OPENROUTER_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENROUTER_TEXT_MAX_TOKENS: int = 8000
    OPENROUTER_VISION_MAX_TOKENS: int = 12000
    PHASH_HAMMING_DISTANCE_THRESHOLD: int = 4
    PHASH_CACHE_MAX_CANDIDATES: int = 300
    # 60 minutes * 24 hours * 20 days = 20  days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 20
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str = "Leaf Disease Detection API"


settings = Settings()  # type: ignore

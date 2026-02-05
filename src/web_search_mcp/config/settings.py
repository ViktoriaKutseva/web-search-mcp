from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings.
    """
    app_version: str = Field(default="0.1.1", description="Application version")
    SEARXNG_BASE_URL: str = "http://localhost:8080"
    SEARXNG_TIMEOUT: int = 10
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

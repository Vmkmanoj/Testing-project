from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings

    Loads configuration from the .env file and provides
    strongly typed access throughout the application.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ----------------------------
    # Application
    # ----------------------------
    APP_NAME: str = Field(...)

    APP_VERSION: str = Field(...)

    APP_ENV: str = Field(...)

    DEBUG: bool = Field(default=False)

    # ----------------------------
    # Database
    # ----------------------------
    DB_HOST: str

    DB_PORT: int

    DB_NAME: str

    DB_USERNAME: str

    DB_PASSWORD: str

    DATABASE_URL: str

    DATABASE_ECHO: bool = False
    
    ALEMBIC_DATABASE_URL: str

    # ----------------------------
    # JWT
    # ----------------------------
    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REFRESH_TOKEN_EXPIRE_DAYS: int

    GROQ_API_KEY: str

    LLM_MODEL: str

    

    ## Origin allowed
    ALLOWED_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
        ]
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache ensures that the .env file is
    loaded only once during application startup.
    """
    return Settings()


settings = get_settings()
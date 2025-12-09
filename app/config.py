from pathlib import Path
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_PORT: int

    @computed_field
    @property
    def TEST_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}"
            f"@{self.TEST_POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
        )

    JWT_SECRET: str
    JWT_ALGORITHM: str

    SMT_HOST: str
    SMT_PORT: int
    SMT_EMAIL: str
    SMT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()


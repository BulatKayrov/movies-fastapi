import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 7777

    REDIS_DB_TOKENS_NAME: str = "tokens"
    REDIS_DB_TOKENS: int = 1

    REDIS_USER_DB: int = 2

    REDIS_DB: int = 0
    REDIS_HASH_KEY_DB: str = "movie-db"


settings = Settings()

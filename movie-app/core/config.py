import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # redis
    REDIS_HOST: str = "redis-movie"
    REDIS_PORT: int = 6379

    # REDIS_HOST: str = getenv("REDIS_HOST", "localhost")
    # REDIS_PORT: int = int(getenv("REDIS_PORT", default=0)) or 7777

    REDIS_DB_TOKENS_NAME: str = "tokens"
    REDIS_DB_TOKENS: int = 1

    REDIS_USER_DB: int = 2

    REDIS_DB: int = 0
    REDIS_HASH_KEY_DB: str = "movie-db"

    # testing env-var for unittest
    TEST_REDIS_HOST: str = "localhost"
    TEST_REDIS_PORT: int = 1234
    TEST_REDIS_DB_TOKENS_NAME: str = "tokens"
    TEST_REDIS_DB_TOKENS: int = 1
    TEST_REDIS_DB_SHORT_URL: int = 0


settings = Settings()

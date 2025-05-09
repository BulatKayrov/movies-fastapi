import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DB_URL: Path = BASE_DIR / "database.json"

    # logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # jwt
    API_TOKENS: frozenset[str] = frozenset(
        {"aK1J-Ez_gQc4iHh8Pa6J-w", "vHOm99YdSFO7c3PuIA6guQ"}
    )
    USER_DB: dict = {"1": "1"}


settings = Settings()

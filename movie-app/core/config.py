from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE: Path = BASE_DIR / "database.json"


settings = Settings()

import secrets
from abc import ABC, abstractmethod
from typing import Awaitable

from redis import Redis

from core.config import settings


class AbstractTokenHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe()

    def generate_token_and_save(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> set[str]:
        pass

    @abstractmethod
    def delete_token(self, token: str) -> None:
        pass


class RedisTokenHelper(AbstractTokenHelper):
    def __init__(
        self, host: str, port: int, redis_db: int, tokens_set_name: str
    ) -> None:
        self.redis = Redis(host=host, port=port, decode_responses=True, db=redis_db)
        self.token_set = tokens_set_name

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.token_set, token))

    def add_token(self, token):
        self.redis.sadd(self.token_set, token)

    def get_tokens(self) -> Awaitable[set] | set:
        return self.redis.smembers(self.token_set)

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.token_set, token)

    def create(self) -> str:
        token = self.generate_token_and_save()
        return token


redis_tokens_helper = RedisTokenHelper(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    redis_db=settings.REDIS_DB_TOKENS,
    tokens_set_name=settings.REDIS_DB_TOKENS_NAME,
)

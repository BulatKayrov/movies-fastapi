from abc import ABC, abstractmethod

from redis import Redis

from core.config import settings


class AbstractUserHelper(ABC):

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        pass

    @classmethod
    def verify_password(cls, password1: str, password2: str) -> bool:
        """
        password1 - password from database
        password2 - raw password
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        password_db = self.get_user_password(username)
        if password_db is None:
            return False
        return self.verify_password(password1=password_db, password2=password)


class RedisUserHelper(AbstractUserHelper):
    def __init__(
        self,
        host: str,
        port: int,
        redis_db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            decode_responses=True,
            db=redis_db,
        )

    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(username)


redis_auth_helper = RedisUserHelper(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    redis_db=settings.REDIS_USER_DB,
)

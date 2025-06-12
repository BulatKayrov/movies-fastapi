import unittest

from api.v1.movie.auth.service.token_service import RedisTokenHelper
from core.config import settings

redis_tokens_test_service = RedisTokenHelper(
    host=settings.TEST_REDIS_HOST,
    port=settings.TEST_REDIS_PORT,
    redis_db=settings.TEST_REDIS_DB_TOKENS,
    tokens_set_name=settings.TEST_REDIS_DB_TOKENS_NAME,
)


class RedisTokensHelperTestCase(unittest.TestCase):

    def test_tokens_create_and_save(self):
        token = redis_tokens_test_service.generate_token_and_save()
        self.assertIsNotNone(token)
        expected = redis_tokens_test_service.token_exists(token)
        self.assertTrue(expected)

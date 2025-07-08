import unittest

from api.v1.movie.service.token_service import redis_tokens_helper

# if getenv("TESTING") != "1":
#     raise OSError('Environment variable TESTING must be set to "1"')


class RedisTokensHelperTestCase(unittest.TestCase):

    def test_tokens_create_and_save(self) -> None:
        token = redis_tokens_helper.generate_token_and_save()
        self.assertIsNotNone(token)
        expected = redis_tokens_helper.token_exists(token)
        self.assertTrue(expected)

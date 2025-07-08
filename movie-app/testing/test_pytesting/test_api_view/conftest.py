import pytest
from api.v1.movie.service import redis_tokens_helper
from main import app
from starlette.testclient import TestClient


@pytest.fixture(scope="package")
def token():
    token = redis_tokens_helper.generate_token_and_save()
    yield token
    redis_tokens_helper.delete_token(token)


@pytest.fixture(scope="package")
def auth_client(token: str):
    with TestClient(app=app) as client:
        client.headers["Authorization"] = f"Bearer {token}"
        yield client

import uuid
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette.testclient import TestClient

from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMovie, SMovieCreate
from api.v1.movie.service import redis_tokens_helper
from main import app


def create_movie(
    slug: str = uuid.uuid4().hex[:10], title: str = uuid.uuid4().hex[:10]
) -> SMovie:
    return storage.create(
        data=SMovieCreate(
            slug=slug, title=title, description="This is a test movie", year=1990
        )
    )


@pytest.fixture(params=[pytest.param(("custom_slug", "custom_title"), id="custom")])
def movie(request: SubRequest) -> SMovie:
    slug, title = request.param
    print(request.param)
    return create_movie(title=title, slug=slug)


@pytest.fixture(scope="package")
def token() -> Generator[str, None]:
    token = redis_tokens_helper.generate_token_and_save()
    yield token
    redis_tokens_helper.delete_token(token)


@pytest.fixture(scope="package")
def auth_client(token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {token}"}
    with TestClient(app=app, headers=headers) as client:
        yield client

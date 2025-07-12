from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMovie
from main import app
from testing.test_pytesting.test_api_view.conftest import create_movie


class TestUpdateIndirectAPIView:

    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[SMovie, None]:
        slug, title = request.param
        yield create_movie(slug=slug, title=title)
        storage.delete_by_slug(slug=slug)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                ("slug_1", "title_1"), "Это просто описание #1", id="custom #1"
            ),
            pytest.param(
                ("slug_2", "title_2"), "Это просто описание #2", id="custom #2"
            ),
        ],
        indirect=["movie"],
    )
    def test_indirect_update_api_view(
        self, auth_client: TestClient, movie: SMovie, new_description: str
    ) -> None:
        url = app.url_path_for("movie:partial_update", slug=movie.slug)
        response = auth_client.patch(
            url, json={"title": "indirect_title", "description": new_description}
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        new_obj = storage.find_by_slug(slug=movie.slug)
        assert new_obj.title == "indirect_title"
        assert new_obj.description == new_description

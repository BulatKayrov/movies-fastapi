import pytest
from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMoviePartialUpdate, SMovieUpdate
from main import app
from starlette.testclient import TestClient

_mock_data = [
    {
        "title": "title_5",
        "slug": "slug89",
        "description": "description_1",
        "year": 1990,
    },
    {
        "title": "title_7",
        "slug": "slug99",
        "description": "description_2",
        "year": 1995,
    },
]


@pytest.mark.parametrize("data", _mock_data)
def test_create_api_view(auth_client: TestClient, data: dict):
    url = app.url_path_for("movie:create")
    response = auth_client.post(url, json=data)
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


def test_get_all_movie(auth_client: TestClient):
    url = app.url_path_for("movie:find_all")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize(
    "slug, data",
    [("slug89", SMoviePartialUpdate(title="new title"))],
)
def test_partial_update_movie(
    auth_client: TestClient, slug: str, data: SMoviePartialUpdate
):
    url = app.url_path_for("movie:partial_update", slug=slug)
    response = auth_client.patch(url, json=data.model_dump())
    assert response.status_code == 200
    assert response.json()["title"] == "new title"


@pytest.mark.parametrize(
    "data",
    [SMovieUpdate(title="full update", description="full description", year=2000)],
)
def test_put_update_movie(auth_client: TestClient, data: SMovieUpdate):
    url = app.url_path_for("movie:update", slug="slug99")
    response = auth_client.put(url, json=data.model_dump())
    assert response.status_code == 200
    assert response.json()["title"] == "full update"


@pytest.mark.parametrize(
    "slug",
    [
        "slug89",
        "slug99",
    ],
)
def test_delete_movie(auth_client: TestClient, slug: str):
    url = app.url_path_for("movie:delete", slug=slug)
    response = auth_client.delete(url)
    assert response.status_code == 204


def test_create_existing_movie(auth_client: TestClient):
    url = app.url_path_for("movie:create")
    response = auth_client.post(url, json=_mock_data[0])
    assert response.status_code == 200


def test_status_code_409(auth_client: TestClient):
    response = auth_client.post(
        url=app.url_path_for("movie:create"), json=_mock_data[0]
    )
    assert response.status_code == 409
    storage.delete_by_slug(_mock_data[0]["slug"])

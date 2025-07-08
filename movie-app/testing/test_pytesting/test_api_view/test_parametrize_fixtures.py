from api.v1.movie.crud import storage
from api.v1.movie.schemas import SMovie
from main import app
from starlette import status
from starlette.testclient import TestClient


def test_create_movie_params(auth_client: TestClient, movie: SMovie):
    url = app.url_path_for("movie:delete", slug=movie.slug)
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(slug=movie.slug)

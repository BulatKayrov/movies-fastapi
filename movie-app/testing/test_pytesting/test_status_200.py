from main import app
from starlette.testclient import TestClient


def test_status_200():
    client = TestClient(app)
    url = app.url_path_for("status_code_200")
    response = client.get(url)
    assert response.status_code == 200

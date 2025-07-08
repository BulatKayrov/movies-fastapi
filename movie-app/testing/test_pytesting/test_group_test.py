from main import app
from starlette.testclient import TestClient


class TestStatusCodeView:

    def test_status_200(self) -> None:
        client = TestClient(app)
        url = app.url_path_for("status_code_200")
        response = client.get(url)
        assert response.status_code == 200

    def test_response_status_code_200(self) -> None:
        client = TestClient(app)
        url = app.url_path_for("status_code_200")
        response = client.get(url)
        assert response.json() == {"status_code": 200}

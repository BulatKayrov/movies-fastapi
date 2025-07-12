import pytest
from starlette.testclient import TestClient

from main import app


@pytest.mark.apitest
def test_status_200() -> None:
    client = TestClient(app)
    url = app.url_path_for("status_code_200")
    response = client.get(url)
    assert response.status_code == 200

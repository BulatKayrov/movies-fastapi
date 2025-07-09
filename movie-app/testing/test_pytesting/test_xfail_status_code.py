import pytest
from main import app
from starlette.testclient import TestClient


@pytest.mark.xfail(reason="xfail not implemented yet", raises=AssertionError)
@pytest.mark.apitest
def test_status_200_version_2() -> None:
    client = TestClient(app)
    url = app.url_path_for("status_code_200")
    response = client.get(url)
    assert response.status_code == 404

from os import getenv

import pytest


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("testing") != "1":
        pytest.exit("Environment is not ready for testing")
        # pytest.fail("Environment is not ready for testing")

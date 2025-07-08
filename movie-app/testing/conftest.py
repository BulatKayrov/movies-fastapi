from os import getenv

import pytest

if getenv("testing") != "1":
    pytest.exit("Environment is not ready for testing")

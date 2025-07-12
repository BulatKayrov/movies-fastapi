import sys

import pytest


@pytest.mark.skip(reason="not implemented yet")
def test_other_schema() -> None:
    other_schema = {"username": "No name"}
    assert other_schema["username"] == "Bob"


@pytest.mark.skipif(sys.version_info < (3, 12), reason="requires Python 3.12 or higher")
def test_other_schema_skipif():
    pass


@pytest.mark.skipif(sys.platform == "win32", reason="requires platform win32 or higher")
def test_other_schema_skipif_v2():
    """Пропустить этот тест, если платформа Windows (потому что требуется не-Windows или более новая версия)"""
    assert sys.platform != "win32"

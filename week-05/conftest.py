"""Start the practice API for every test in week 5.

Students point their code at http://127.0.0.1:8765. The real thing would be a
real URL; nothing else about the code changes.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

BASE_URL = "http://127.0.0.1:8765"

_spec = importlib.util.spec_from_file_location(
    "week05_server", Path(__file__).parent / "server.py"
)
_server_module = importlib.util.module_from_spec(_spec)
sys.modules["week05_server"] = _server_module
_spec.loader.exec_module(_server_module)


@pytest.fixture(scope="session", autouse=True)
def practice_api():
    """One server for the whole session."""
    server = _server_module.serve_in_background()
    yield BASE_URL
    server.shutdown()


@pytest.fixture
def base_url(practice_api):
    return practice_api


@pytest.fixture
def reset_flaky(practice_api):
    """/flaky fails twice then succeeds. Put it back to the start."""
    import urllib.request

    urllib.request.urlopen(f"{practice_api}/reset-flaky").read()
    yield

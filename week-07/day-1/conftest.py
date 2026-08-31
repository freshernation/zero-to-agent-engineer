"""Make this folder's own modules importable by name - and make sure they are
THIS folder's.

Several days ship a file called toolkit.py. Python caches modules by name, so
whichever one is imported first would otherwise be handed to every later day,
which produces genuinely baffling failures (a tool that exists, reported
missing). Before each test, any cached module of a local name that came from a
different folder is evicted.
"""

import sys
from pathlib import Path

import pytest

_here = Path(__file__).parent
_local_names = {p.stem for p in _here.glob("*.py")} - {"conftest"}

if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))


@pytest.fixture(autouse=True)
def _prefer_this_folders_modules():
    for name in _local_names:
        module = sys.modules.get(name)
        if module is None:
            continue
        origin = getattr(module, "__file__", "") or ""
        if not origin.startswith(str(_here)):
            sys.modules.pop(name, None)
    yield

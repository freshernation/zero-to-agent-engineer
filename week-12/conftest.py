"""Make the week's shared modules importable from every week-10 test."""

import sys
from pathlib import Path

_here = str(Path(__file__).parent)
if _here not in sys.path:
    sys.path.insert(0, _here)

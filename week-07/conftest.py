"""Make fake_model importable from every week-7 test and student file."""

import sys
from pathlib import Path

_here = str(Path(__file__).parent)
if _here not in sys.path:
    sys.path.insert(0, _here)

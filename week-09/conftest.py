"""Make retrieval_kit and the corpus reachable from every week-9 test."""

import sys
from pathlib import Path

_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

CORPUS = _here / "corpus"

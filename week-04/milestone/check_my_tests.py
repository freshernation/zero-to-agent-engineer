"""Run your own test suite and show its output.

    python3 week-04/milestone/check_my_tests.py

Runs it in a clean copy of this folder, the way the grader does.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
NEEDED = ["test_ledger.py", "expense.py", "ledger.py"]

if __name__ == "__main__":
    missing = [n for n in NEEDED if not (HERE / n).exists()]
    if missing:
        print(f"Missing: {', '.join(missing)}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        for name in NEEDED:
            shutil.copy2(HERE / name, Path(tmp) / name)
        subprocess.run(
            [sys.executable, "-m", "pytest", "test_ledger.py", "-v",
             "--tb=short", "-p", "no:cacheprovider"],
            cwd=tmp,
        )
    print(
        "\nThat is your suite against your own code. Whether it would notice a "
        "broken implementation is what `pytest week-04/milestone` checks."
    )

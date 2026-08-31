"""Run the test suites you wrote today and show their output.

    python3 week-04/day-3/check_my_tests.py

Runs them exactly the way the grader does - in a clean copy of this folder, so
the course's own pytest settings cannot interfere with yours.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
PAIRS = [("test_shapes.py", "shapes.py"), ("test_stats.py", "stats.py")]


def run(test_file, module_file):
    print(f"\n{'=' * 60}\n{test_file}\n{'=' * 60}")
    for name in (test_file, module_file):
        if not (HERE / name).exists():
            print(f"  {name} does not exist yet.")
            return
    with tempfile.TemporaryDirectory() as tmp:
        for name in (test_file, module_file):
            shutil.copy2(HERE / name, Path(tmp) / name)
        subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v",
             "--tb=short", "-p", "no:cacheprovider"],
            cwd=tmp,
        )


if __name__ == "__main__":
    for test_file, module_file in PAIRS:
        run(test_file, module_file)
    print(
        "\nThat is your suite passing on correct code. Whether it would notice a "
        "bug is a different question - `pytest week-04/day-3` answers that one."
    )

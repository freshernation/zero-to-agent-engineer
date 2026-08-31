"""Run one drill, timed.

    python3 week-12/day-2/drill.py            list them
    python3 week-12/day-2/drill.py two_sum    run one

Talk out loud while the timer runs. That is the part being practised.
"""

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent

TARGETS = {
    "two_sum": 6, "most_common_word": 6, "group_by": 5, "top_n_by": 5,
    "running_total": 4, "chunk": 5, "first_duplicate": 5, "invert": 5,
    "is_balanced": 8, "flatten": 7,
}


def main():
    if len(sys.argv) < 2:
        print("Drills:\n")
        for name, minutes in TARGETS.items():
            print(f"  {name:<20} {minutes} min")
        print("\n  python3 week-12/day-2/drill.py <name>")
        return 0

    name = sys.argv[1]
    if name not in TARGETS:
        print(f"No drill called {name}. Run with no arguments to list them.")
        return 1

    print(f"\n{name} - target {TARGETS[name]} minutes")
    print("Talk out loud. Say the edge cases before you are asked.")
    input("Press Enter when you are ready to start, and again when you are done.")

    started = time.monotonic()
    input("...running. Enter when finished.")
    elapsed = time.monotonic() - started

    minutes, seconds = divmod(int(elapsed), 60)
    target = TARGETS[name] * 60
    verdict = "inside target" if elapsed <= target else "over target"
    print(f"\n{minutes}m {seconds}s - {verdict}\n")

    subprocess.run(
        [sys.executable, "-m", "pytest", "test_day2.py", "-q", "-k", name,
         "-p", "no:cacheprovider"],
        cwd=str(HERE),
    )
    print("\nAdd a line to DRILL_LOG.md: which drill, how long, what slowed you down.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Day-zero environment check.

Run this with:  python3 check_setup.py

Every line should say OK. If one says FAIL, it tells you what to do about it.
You are not expected to understand this file. It is the only code in the course
you did not write.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"
OFF = "\033[0m"

results = []


def check(name, ok, fix=""):
    results.append((name, ok, fix))
    tag = f"{GREEN}OK  {OFF}" if ok else f"{RED}FAIL{OFF}"
    print(f"  {tag}  {name}")
    if not ok and fix:
        print(f"        {DIM}-> {fix}{OFF}")


def main():
    print("\nChecking your setup\n" + "-" * 46)

    # 1. Python version
    v = sys.version_info
    check(
        f"Python {v.major}.{v.minor}.{v.micro}",
        (v.major, v.minor) >= (3, 12),
        "Install Python 3.12 or newer - see SETUP.md step 2.",
    )

    # 2. Virtual environment active
    in_venv = sys.prefix != sys.base_prefix
    check(
        "Virtual environment is active",
        in_venv,
        "Run:  source .venv/bin/activate   (Windows: .venv\\Scripts\\Activate.ps1)",
    )

    # 3. The venv belongs to this project
    if in_venv:
        check(
            "Virtual environment belongs to this repo",
            Path(sys.prefix).resolve().parent == ROOT,
            f"You are in a venv, but not this project's. Expected {ROOT / '.venv'}.",
        )

    # 4. pytest installed
    try:
        import pytest  # noqa: F401
        has_pytest = True
    except ImportError:
        has_pytest = False
    check(
        "pytest is installed",
        has_pytest,
        "Run:  pip install -r requirements.txt",
    )

    # 5. git available
    check(
        "git is installed",
        shutil.which("git") is not None,
        "Install git - see SETUP.md step 4.",
    )

    # 6. git identity configured
    name = email = ""
    if shutil.which("git"):
        def cfg(key):
            r = subprocess.run(
                ["git", "config", "--global", key],
                capture_output=True, text=True,
            )
            return r.stdout.strip()
        name, email = cfg("user.name"), cfg("user.email")
    check(
        f"git knows who you are{f' ({name})' if name else ''}",
        bool(name and email),
        'Run:  git config --global user.name "Your Name"  and the same for user.email',
    )

    # 7. Can actually run a script
    try:
        r = subprocess.run(
            [sys.executable, "-c", "print('hello')"],
            capture_output=True, text=True, timeout=10,
        )
        can_run = r.stdout.strip() == "hello"
    except Exception:
        can_run = False
    check(
        "Python can run a script",
        can_run,
        "Something is deeply wrong. Send this whole output to your instructor.",
    )

    print("-" * 46)
    failed = [r for r in results if not r[1]]
    if failed:
        print(f"\n{RED}{len(failed)} check(s) failed.{OFF} Fix the ones above, "
              f"then run this again.\n"
              f"Stuck for more than 20 minutes? Message your instructor - "
              f"setup is the one place struggling teaches you nothing.\n")
        return 1

    print(f"\n{GREEN}All checks passed.{OFF} You are ready.\n"
          f"Next: open week-01/README.md\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

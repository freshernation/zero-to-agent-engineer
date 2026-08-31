"""Everything here carries type hints.

    total(prices: list) -> float                    sum, rounded to 2dp
    label(name: str, amount: float) -> str          "Coffee: $4.50"
    find(names: list, target: str) -> int           position, or -1
    first_match(names: list, letter: str) -> Optional[str]
                                                    first name starting with letter,
                                                    or None

    class Task:
        __init__(self, title: str, done: bool = False) -> None
        complete(self) -> None
        summary(self) -> str        "[x] Write tests" / "[ ] Write tests"

from typing import Optional
"""

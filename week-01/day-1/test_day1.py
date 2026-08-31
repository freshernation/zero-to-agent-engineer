"""Day 1 - print, strings, escapes.

Run me:  pytest week-01/day-1 -v
"""

RECEIPT = [
    "=========================",
    "     THE CORNER CAFE",
    "=========================",
    "Flat white           3.40",
    "Croissant            2.75",
    "-------------------------",
    "TOTAL                6.15",
    "=========================",
]


class TestHello:
    def test_first_line_is_exact(self, run):
        r = run("hello.py")
        assert r.line(0) == "Hello, world!", (
            f"Line 1 should be exactly 'Hello, world!' but was {r.line(0)!r}. "
            "Check the capital H, the comma, and the exclamation mark."
        )

    def test_prints_three_lines(self, run):
        r = run("hello.py")
        assert len(r.lines) == 3, (
            f"Expected exactly 3 lines, got {len(r.lines)}:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_name_and_reason_are_not_empty(self, run):
        r = run("hello.py")
        assert r.line(1).strip(), "Line 2 should be your name."
        assert r.line(2).strip(), "Line 3 should be why you are doing this course."


class TestReceipt:
    def test_line_count(self, run):
        r = run("receipt.py")
        assert len(r.lines) == 8, (
            f"The receipt is 8 lines. You printed {len(r.lines)}:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_every_line_matches(self, run):
        r = run("receipt.py")
        for i, expected in enumerate(RECEIPT):
            actual = r.line(i)
            assert actual == expected, (
                f"Line {i + 1} does not match.\n"
                f"  expected |{expected}|  ({len(expected)} chars)\n"
                f"  yours    |{actual}|  ({len(actual)} chars)\n"
                "Count the spaces. The banner is 25 wide and prices end at column 25."
            )


class TestEscapes:
    def test_quotes(self, run):
        r = run("escapes.py")
        assert r.line(0) == 'She said "hello" and left.', (
            f"Line 1 was {r.line(0)!r}. It needs real double quotes around hello."
        )

    def test_backslashes(self, run):
        r = run("escapes.py")
        assert r.line(1) == r"Path: C:\Users\new", (
            f"Line 2 was {r.line(1)!r}. A single backslash is an instruction - "
            r"\U and \n are doing something you did not intend. "
            "You need two backslashes to print one."
        )

    def test_tab(self, run):
        r = run("escapes.py")
        assert r.line(2) == "Name\tScore", (
            f"Line 3 was {r.line(2)!r}. That gap must be a real tab (\\t), not spaces."
        )

    def test_uses_three_prints(self, source):
        count = source("escapes.py").count("print(")
        assert count == 3, (
            f"Use exactly 3 print() calls - you used {count}."
        )

"""Week 3, Day 4 - comprehensions and cross-function bugs.

Run me:  pytest week-03/day-4 -v
"""

import ast
import pytest

PLACEHOLDER = "(your answer)"

RECORDS = [
    {"name": "Ana", "amount": 40},
    {"name": "Ben", "amount": 90},
    {"name": "Cara", "amount": 15},
    {"name": "Dev", "amount": 70},
]


class TestComprehensions:
    def test_doubled(self, load):
        c = load("comprehend.py")
        assert c.doubled([1, 2, 3]) == [2, 4, 6]
        assert c.doubled([]) == []
        assert c.doubled([-2, 0]) == [-4, 0]

    def test_long_words_default(self, load):
        c = load("comprehend.py")
        assert c.long_words(["hi", "hello", "hey", "welcome"]) == ["hello", "welcome"]

    def test_long_words_custom_length(self, load):
        c = load("comprehend.py")
        assert c.long_words(["hi", "hey"], 2) == ["hi", "hey"]
        assert c.long_words(["hi", "hey"], min_length=3) == ["hey"]

    def test_names_only(self, load):
        c = load("comprehend.py")
        assert c.names_only(RECORDS) == ["Ana", "Ben", "Cara", "Dev"]
        assert c.names_only([]) == []

    def test_price_map(self, load):
        c = load("comprehend.py")
        items = [
            {"name": "Tea", "price": 2.5},
            {"name": "Cake", "price": 4.0},
        ]
        assert c.price_map(items) == {"Tea": 2.5, "Cake": 4.0}

    def test_top_n(self, load):
        c = load("comprehend.py")
        top = c.top_n(RECORDS, 2)
        assert [r["name"] for r in top] == ["Ben", "Dev"], (
            f"Expected Ben then Dev, got {[r.get('name') for r in top]}. "
            "Highest amount first."
        )

    def test_top_n_returns_whole_records(self, load):
        c = load("comprehend.py")
        top = c.top_n(RECORDS, 1)
        assert top == [{"name": "Ben", "amount": 90}], (
            "top_n returns the records themselves, not just their names."
        )

    def test_top_n_handles_n_bigger_than_the_list(self, load):
        c = load("comprehend.py")
        assert len(c.top_n(RECORDS, 99)) == 4

    def test_actually_used_comprehensions(self, source):
        """Counted from the parsed syntax tree, not by searching the text -
        so nested brackets and strings cannot fool it either way."""
        tree = ast.parse(source("comprehend.py"))
        found = sum(
            isinstance(node, (ast.ListComp, ast.DictComp,
                              ast.SetComp, ast.GeneratorExp))
            for node in ast.walk(tree)
        )
        assert found >= 4, (
            f"Found {found} comprehension(s), expected at least 4. "
            "doubled, long_words, names_only and price_map should each be one - "
            "that is what today is for. (top_n should not be.)"
        )


class TestFixes:
    def test_broken_1_returns_instead_of_printing(self, run, source):
        run("broken_1.py").expect("Grand total with tax: 64.80")
        code = source("broken_1.py", code_only=True)
        assert "return total" in code.replace("  ", " "), (
            "The fix is for calculate_total to return its answer rather than "
            "print it. Do not work around it at the call site."
        )

    def test_broken_2_counter(self, run):
        run("broken_2.py").expect("Counter: 3")

    def test_broken_2_is_not_hard_coded(self, run, source):
        run("broken_2.py").expect("Counter: 3")
        code = source("broken_2.py", code_only=True)
        assert "counter = 3" not in code.replace("  ", " "), (
            "Do not set the counter to 3. The function has to take a value in "
            "and hand the new one back."
        )
        assert code.count("add_one(") >= 4, (
            "Keep all three calls to add_one. The fix is in how the value gets "
            "back out of the function, not in deleting the calls."
        )

    def test_broken_3_catches_the_right_exception(self, run, source):
        r = run("broken_3.py")
        r.expect("5.0")
        r.expect("Cannot divide by zero")
        code = source("broken_3.py", code_only=True)
        for bad in ("except:", "except Exception:"):
            assert bad not in code, (
                f"Found `{bad}`. That works, and it also hides every other "
                "mistake in the block. Catch ZeroDivisionError by name."
            )


class TestNotes:
    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_entry_is_filled_in(self, source, n):
        text = source("NOTES.md")
        parts = text.split(f"## broken_{n}.py")
        assert len(parts) > 1, f"NOTES.md is missing the broken_{n}.py section."
        body = parts[1].split("\n## ")[0]
        assert PLACEHOLDER not in body, (
            f"The broken_{n}.py entry still has '{PLACEHOLDER}' placeholders."
        )
        words = len(body.split())
        assert words >= 40, (
            f"The broken_{n}.py entry is only {words} words. Answer all four "
            "prompts properly, in your own words."
        )

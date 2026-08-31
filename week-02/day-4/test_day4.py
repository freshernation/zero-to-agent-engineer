"""Week 2, Day 4 - tuples, sets, zip, sorting, and three more bugs.

Run me:  pytest week-02/day-4 -v

Some of these tests swap the data in your file for a different set and check the
output follows. Leave the data block at the top exactly as it was given to you.
"""

import pytest

PLACEHOLDER = "(your answer)"


class TestUnique:
    def test_counts(self, run):
        r = run("unique.py")
        r.expect("Total visits: 7")
        r.expect("Unique visitors: 4")

    def test_names_are_sorted(self, run):
        run("unique.py").expect("Names: ['ana', 'ben', 'cara', 'dev']")

    def test_same_answer_every_run(self, run):
        """A bare set() prints in an unpredictable order. sorted() fixes it."""
        run("unique.py").require_output()
        outputs = {run("unique.py").stdout for _ in range(4)}
        assert len(outputs) == 1, (
            "Your program printed different things on different runs. A set has no "
            "reliable order - wrap it in sorted() before you print it."
        )

    def test_works_with_other_data(self, run_variant):
        r = run_variant("unique.py", {
            '["ana", "ben", "ana", "cara", "ben", "ana", "dev"]':
            '["zoe", "zoe", "amy"]'
        })
        r.expect("Total visits: 3")
        r.expect("Unique visitors: 2")
        r.expect("Names: ['amy', 'zoe']")


class TestPairs:
    def test_output(self, run):
        r = run("pairs.py")
        assert r.lines == [
            "Widget: $4.50",
            "Gadget: $12.00",
            "Doohickey: $3.25",
        ], (
            "Expected one line per product, got:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_uses_zip(self, source):
        code = source("pairs.py", code_only=True)
        assert "zip(" in code, "Use zip() to walk the two lists together."
        assert "range(len(" not in code.replace(" ", ""), (
            "You have zip() now - looping over positions with range(len(...)) is "
            "the thing it replaces."
        )


class TestRanking:
    def test_top_three(self, run):
        r = run("ranking.py")
        r.expect("1. Ben          892")
        r.expect("2. Dev          733")
        r.expect("3. Cara         615")

    def test_summary(self, run):
        r = run("ranking.py")
        r.expect("Winner: Ben")
        r.expect("Spread: 764")

    def test_only_three_are_ranked(self, run):
        r = run("ranking.py")
        r.expect("1. ")
        assert "4." not in r.stdout and "Eve" not in r.stdout, (
            "Top three only. Ana and Eve should not appear in the ranking."
        )

    def test_works_with_other_players(self, run_variant):
        r = run_variant("ranking.py", {
            'players = ["Ana", "Ben", "Cara", "Dev", "Eve"]':
            'players = ["Kim", "Lee", "Max", "Nia", "Omar"]',
            "scores = [340, 892, 615, 733, 128]":
            "scores = [10, 50, 20, 40, 30]",
        })
        r.expect("1. Lee           50")
        r.expect("2. Nia           40")
        r.expect("3. Omar          30")
        r.expect("Winner: Lee")
        r.expect("Spread: 40")


class TestFixes:
    def test_broken_1_index_error(self, run):
        r = run("broken_1.py")
        assert r.lines == ["a", "b", "c"], (
            f"Expected a, b, c on three lines. Got: {r.lines}"
        )

    def test_broken_2_key_error(self, run):
        r = run("broken_2.py")
        r.expect("Ana 30")
        r.expect("Ben 25")

    def test_broken_3_accumulator_reset(self, run):
        run("broken_3.py").expect("Total: 20")

    def test_broken_3_is_actually_calculated(self, run_variant):
        """Moving the reset out of the loop fixes it. Typing 20 in does not."""
        r = run_variant("broken_3.py", {"prices = [5, 7, 8]": "prices = [1, 2, 3, 4]"})
        r.expect("Total: 10")


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

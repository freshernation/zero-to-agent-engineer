"""Day 4 - debugging.

Run me:  pytest week-01/day-4 -v

Before you fix a file, run it yourself and read the error. The tests will tell you
what broke, but reading the traceback with your own eyes is the entire exercise.
"""

import pytest

PLACEHOLDER = "(your answer)"


class TestFixes:
    def test_broken_1_syntax_error(self, run):
        run("broken_1.py").expect("Hello, Sam")

    def test_broken_2_name_error(self, run):
        run("broken_2.py").expect("Average: 8.0")

    def test_broken_3_type_error(self, run):
        run("broken_3.py").expect("You are 30 years old.")

    def test_broken_4_indentation_error(self, run, source):
        run("broken_4.py").expect("Pass")
        assert "if" in source("broken_4.py"), (
            "Deleting the 'if' makes the test pass and teaches you nothing. "
            "The condition has to stay - fix the indentation instead."
        )

    def test_broken_5_logic_error(self, run, source):
        run("broken_5.py").expect("Area: 21")
        text = source("broken_5.py")
        assert "21" not in text, (
            "Do not hard-code 21. The width and height stay as they are - "
            "the calculation between them is what is wrong."
        )


class TestNotes:
    """The notes are the real deliverable. Fixing five bugs by trial and error
    teaches you much less than writing down what each error meant."""

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
    def test_entry_is_filled_in(self, source, n):
        text = source("NOTES.md")
        section = text.split(f"## broken_{n}.py")
        assert len(section) > 1, f"NOTES.md is missing the broken_{n}.py section."
        body = section[1].split("\n## ")[0]
        assert PLACEHOLDER not in body, (
            f"The broken_{n}.py entry in NOTES.md still has "
            f"'{PLACEHOLDER}' placeholders in it."
        )
        words = len(body.split())
        assert words >= 40, (
            f"The broken_{n}.py entry is only {words} words. "
            "Answer all four prompts properly - in your own words, "
            "not by pasting the error message."
        )

    def test_question_for_the_live_hour(self, source):
        tail = source("NOTES.md").split("One question for the live hour")[-1]
        assert "(Write down" not in tail and len(tail.split()) >= 8, (
            "Write down the thing you are least sure about, at the bottom of "
            "NOTES.md. Your instructor uses these to plan Friday."
        )

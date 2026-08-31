"""Week 13, Day 4 - keeping the repo warm.

Run me:  pytest week-13/day-4 -v
"""

import re

import pytest

HEADINGS = ["What I changed", "Before and after", "What it cost", "The habit"]


def shipped(source, heading=None):
    text = re.sub(r"<!--.*?-->", "", source("SHIPPED.md"), flags=re.S)
    if heading is None:
        return text
    assert f"## {heading}" in text, f"SHIPPED.md has no '{heading}' section."
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestChangelog:
    def test_has_a_dated_entry(self, source):
        text = re.sub(r"<!--.*?-->", "", source("CHANGELOG.md"), flags=re.S)
        dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", text, flags=re.M)
        assert dates, (
            "No dated entry. A repository whose last commit is the day the "
            "course ended says 'this was homework'."
        )

    def test_the_entry_is_written(self, source):
        text = re.sub(r"<!--.*?-->", "", source("CHANGELOG.md"), flags=re.S)
        entries = re.split(r"^## \d{4}-\d{2}-\d{2}", text, flags=re.M)[1:]
        assert entries, "No entry body."
        assert len(entries[0].split()) >= 25, (
            "The entry is too short. What changed, what it did to the number, "
            "and why - three sentences."
        )

    def test_the_entry_has_a_number(self, source):
        text = re.sub(r"<!--.*?-->", "", source("CHANGELOG.md"), flags=re.S)
        entries = re.split(r"^## \d{4}-\d{2}-\d{2}", text, flags=re.M)[1:]
        assert re.search(r"\d", entries[0]), (
            "No number in the entry. Even 'unchanged' needs the figure it did "
            "not change from - and an honest 'tried X, no difference, reverted' "
            "reads better than a claim with nothing behind it."
        )

    def test_placeholder_gone(self, source):
        assert "YYYY-MM-DD" not in source("CHANGELOG.md")


class TestShipped:
    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        assert len(shipped(source, heading).split()) >= 30, (
            f"'{heading}' is too short."
        )

    def test_before_and_after_has_two_numbers(self, source):
        section = shipped(source, "Before and after")
        numbers = re.findall(r"\d+\.?\d*", section)
        assert len(numbers) >= 2, (
            "Both numbers. Running the eval before and after is what turns a "
            "change into evidence."
        )

    def test_the_habit_is_specific(self, source):
        section = shipped(source, "The habit").lower()
        assert any(
            word in section
            for word in ("week", "weekly", "monday", "tuesday", "wednesday",
                         "thursday", "friday", "saturday", "sunday", "every")
        ), (
            "Say when. 'I'll keep improving it' is not a habit; 'one commit "
            "every Sunday evening' is."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("SHIPPED.md")

"""Week 13, Day 1 - the gap.

Run me:  pytest week-13/day-1 -v
"""

import re

import pytest

HEADINGS = [
    "The number",
    "Why it is weakest",
    "What I did about it",
    "The evidence",
]

DIMENSIONS = ("correctness", "structure", "specificity", "confidence")


def body(source):
    text = re.sub(r"<!--.*?-->", "", source("GAP.md"), flags=re.S)
    for heading in HEADINGS:
        text = text.replace(f"## {heading}", "")
    return text


class TestGap:
    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("GAP.md")
        assert f"## {heading}" in text, f"GAP.md has no '{heading}' section."
        section = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(section.split()) >= 30, (
            f"'{heading}' is {len(section.split())} words."
        )

    def test_long_enough(self, source):
        assert len(body(source).split()) >= 250

    def test_has_numbers(self, source):
        assert len(re.findall(r"\d+\.?\d*", body(source))) >= 2, (
            "At least two numbers. The score you started from and something "
            "about where you got to - this document is evidence, not a resolution."
        )

    def test_names_one_dimension(self, source):
        text = body(source).lower()
        named = [d for d in DIMENSIONS if d in text]
        assert named, (
            "GAP.md does not name any of the four dimensions. Say which one is "
            "lowest."
        )

    def test_focuses_on_one(self, source):
        """A bit of everything produces a bit of nothing."""
        section = source("GAP.md").split("## What I did about it", 1)
        assert len(section) > 1
        text = section[1].split("\n## ")[0].lower()
        assert len(text.split()) >= 30, "Write the section first."
        named = [d for d in DIMENSIONS if d in text]
        assert len(named) <= 2, (
            f"'What I did about it' works on {named}. One dimension. A single "
            "score moved from 2.9 to 3.6 changes more interviews than four "
            "moved by a tenth."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("GAP.md")

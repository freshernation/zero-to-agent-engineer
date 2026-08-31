"""Week 13, Day 3 - outreach.

Run me:  pytest week-13/day-3 -v
"""

import re

import pytest

HEADINGS = ["The list", "Sent", "Replies", "What I would change"]


def body(source):
    return re.sub(r"<!--.*?-->", "", source("OUTREACH.md"), flags=re.S)


def section(source, heading):
    text = body(source)
    assert f"## {heading}" in text, f"OUTREACH.md has no '{heading}' section."
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheList:
    def test_ten_names(self, source):
        rows = [
            line for line in section(source, "The list").splitlines()
            if line.strip().startswith("|") and "---" not in line
            and "Name" not in line and line.split("|")[1].strip()
        ]
        assert len(rows) >= 10, (
            f"{len(rows)} names. Most people stop at four and the list is closer "
            "to twenty - write everyone down before judging any of them."
        )

    def test_every_row_has_a_specific_ask(self, source):
        self.test_ten_names(source)  # nothing to check until the list exists
        rows = [
            line for line in section(source, "The list").splitlines()
            if line.strip().startswith("|") and "---" not in line
            and "Name" not in line and line.split("|")[1].strip()
        ]
        vague = [
            row for row in rows
            if len(row.split("|")[4].strip().split()) < 4
        ]
        assert not vague, (
            f"{len(vague)} rows have no real ask in them. 'Let me know if you "
            "hear of anything' gets forgotten by lunchtime because there is "
            "nothing to do with it."
        )


class TestSent:
    def test_at_least_five(self, source):
        text = section(source, "Sent")
        entries = [
            line for line in text.splitlines()
            if line.strip().startswith(("-", "*", "|", "1.", "2.", "3.", "4.", "5."))
            and len(line.split()) >= 4
        ]
        assert len(entries) >= 5, (
            f"{len(entries)} sent. Five today - this is the channel your own "
            "numbers said converts best."
        )


class TestReflection:
    @pytest.mark.parametrize("heading", ["Replies", "What I would change"])
    def test_written(self, source, heading):
        assert len(section(source, heading).split()) >= 40, (
            f"'{heading}' is too short."
        )

    def test_counts_the_silences(self, source):
        text = section(source, "Replies").lower()
        assert any(
            word in text for word in ("no reply", "silence", "nothing", "not heard",
                                      "no response", "yet")
        ), (
            "Record the silences too. A reply rate you cannot calculate is a "
            "channel you cannot judge."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("OUTREACH.md")

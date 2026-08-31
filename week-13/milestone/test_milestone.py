"""Week 13 milestone - the plan.

Run me:  pytest week-13/milestone -v
"""

import re

import pytest

HEADINGS = [
    "Where I am",
    "The weekly rhythm",
    "What I am still weakest at",
    "What I do if nothing lands in six weeks",
    "What I am not going to do",
]

DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday", "every week", "weekly", "each week")


def body(source):
    text = re.sub(r"<!--.*?-->", "", source("NEXT.md"), flags=re.S)
    for heading in HEADINGS:
        text = text.replace(f"## {heading}", "")
    return text


def section(source, heading):
    text = re.sub(r"<!--.*?-->", "", source("NEXT.md"), flags=re.S)
    assert f"## {heading}" in text, f"NEXT.md has no '{heading}' section."
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestStructure:
    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        assert len(section(source, heading).split()) >= 40, (
            f"'{heading}' is {len(section(source, heading).split())} words."
        )

    def test_long_enough(self, source):
        assert len(body(source).split()) >= 400

    def test_has_numbers(self, source):
        assert len(re.findall(r"\d+\.?\d*", body(source))) >= 4, (
            "At least four numbers. Applications out, responses, interviews, "
            "what you are committing to weekly - a plan without figures is an "
            "intention."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("NEXT.md")


class TestTheRhythmIsReal:
    def test_commitments_have_days(self, source):
        text = section(source, "The weekly rhythm").lower()
        assert any(day in text for day in DAYS), (
            "No day of the week anywhere. 'Keep applying' is not a plan; "
            "'five applications every Tuesday morning' is."
        )

    def test_the_rhythm_covers_the_three_things(self, source):
        text = section(source, "The weekly rhythm").lower()
        missing = []
        if not any(w in text for w in ("appl", "apply")):
            missing.append("applications")
        if not any(w in text for w in ("mock", "interview practice", "practise")):
            missing.append("a mock")
        if not any(w in text for w in ("commit", "ship", "improve", "repo")):
            missing.append("shipping something")
        assert not missing, (
            f"The rhythm misses: {', '.join(missing)}. All three keep going - "
            "applications, one recorded mock, and one commit so the repository "
            "does not freeze."
        )


class TestHonesty:
    def test_the_weakness_comes_from_the_last_mock(self, source):
        text = section(source, "What I am still weakest at")
        assert re.search(r"\d", text), (
            "No number. This should come from mock 11's scores, not from memory."
        )

    def test_the_contingency_is_concrete(self, source):
        text = section(source, "What I do if nothing lands in six weeks")
        assert len(text.split()) >= 60, (
            "The contingency is the section people write in one line and then "
            "need. Say what you would actually change."
        )

    def test_names_what_to_avoid(self, source):
        text = section(source, "What I am not going to do").lower()
        assert any(
            phrase in text
            for phrase in ("project", "framework", "course", "build", "learn")
        ), (
            "The failure mode after a course ends is starting a fourth project "
            "instead of applying, because building is comfortable and rejection "
            "is not. Name the thing you will be tempted by."
        )

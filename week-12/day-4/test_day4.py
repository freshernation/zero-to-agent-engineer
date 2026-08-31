"""Week 12, Day 4 - designing on a whiteboard.

Run me:  pytest week-12/day-4 -v
"""

import re

import pytest
from design_bank import PROMPTS

SECTIONS = [
    "The question I'd ask",
    "The shape",
    "Components",
    "What goes wrong",
    "How I'd know",
]


def body(source):
    return re.sub(r"<!--.*?-->", "", source("DESIGNS.md"), flags=re.S)


def answered_ids(source):
    return [p["id"] for p in PROMPTS if f"## {p['id']}" in body(source)]


def two_answered(source):
    """The ids to check. Fails loudly rather than looping over nothing."""
    answered = answered_ids(source)
    assert len(answered) >= 2, (
        f"Found {len(answered)} answered prompt(s) in DESIGNS.md ({answered}). "
        "Answer two, using the prompt's id from design_bank.py as the heading."
    )
    return answered[:2]


def section_of(source, prompt_id, heading):
    text = body(source).split(f"## {prompt_id}", 1)[1].split("\n## ")[0]
    assert f"### {heading}" in text, (
        f"'{prompt_id}' has no '### {heading}' section."
    )
    return text.split(f"### {heading}", 1)[1].split("\n### ")[0].strip()


class TestTwoAnswered:
    def test_exactly_two(self, source):
        answered = answered_ids(source)
        assert len(answered) >= 2, (
            f"Found {len(answered)} answered ({answered}). Answer two of the "
            "three prompts, using the prompt's id as the heading."
        )

    def test_the_placeholders_are_gone(self, source):
        assert "<first prompt id>" not in body(source), (
            "Replace the placeholder headings with real prompt ids from "
            "design_bank.py."
        )


class TestStructure:
    @pytest.mark.parametrize("heading", SECTIONS)
    def test_every_answer_has_every_section(self, source, heading):
        for prompt_id in two_answered(source):
            content = section_of(source, prompt_id, heading)
            assert content, f"'{prompt_id}' has an empty '{heading}'."

    def test_length(self, source):
        for prompt_id in two_answered(source):
            text = body(source).split(f"## {prompt_id}", 1)[1].split("\n## ")[0]
            words = len(text.split())
            assert 250 <= words <= 600, (
                f"'{prompt_id}' is {words} words. Between 250 and 600 - under is "
                "a sketch, over is more than anybody will listen to."
            )


class TestTheSectionsThatSeparate:
    def test_three_failure_modes(self, source):
        for prompt_id in two_answered(source):
            content = section_of(source, prompt_id, "What goes wrong")
            items = [
                line for line in content.splitlines()
                if line.strip().startswith(("-", "*", "1.", "2.", "3."))
            ]
            assert len(items) >= 3, (
                f"'{prompt_id}' names {len(items)} failure modes. Three, "
                "specifically. This is the section almost nobody volunteers and "
                "the one that separates candidates."
            )

    def test_the_metric_gates_something(self, source):
        for prompt_id in two_answered(source):
            content = section_of(source, prompt_id, "How I'd know").lower()
            assert any(
                word in content
                for word in ("gate", "block", "deploy", "before", "threshold")
            ), (
                f"'{prompt_id}' names a metric but nothing it decides. A number "
                "nobody acts on is a number nobody looks at."
            )

    def test_the_shape_is_one_sentence(self, source):
        for prompt_id in two_answered(source):
            content = section_of(source, prompt_id, "The shape")
            assert len(content.split()) <= 60, (
                f"'{prompt_id}' takes {len(content.split())} words to say the "
                "shape. One sentence - it is the sentence you lead with."
            )

    def test_asks_a_question(self, source):
        for prompt_id in two_answered(source):
            content = section_of(source, prompt_id, "The question I'd ask")
            assert "?" in content, (
                f"'{prompt_id}' has no actual question in it. One question, and "
                "why it matters."
            )


class TestCoverage:
    def test_covers_what_matters(self, source):
        from design_bank import by_id

        for prompt_id in two_answered(source):
            text = body(source).split(f"## {prompt_id}", 1)[1].split("\n## ")[0].lower()
            prompt = by_id(prompt_id)
            missing = [
                " / ".join(options)
                for options in prompt["must_cover"]
                if not any(option.lower() in text for option in options)
            ]
            assert not missing, (
                f"'{prompt_id}' never mentions: {'; '.join(missing)}.\n"
                "These are what somebody who has built one inevitably says."
            )


class TestBank:
    def test_three_prompts(self):
        assert len(PROMPTS) == 3

    def test_by_id(self, load):
        assert load("design_bank.py").by_id("support_bot")["prompt"]
        assert load("design_bank.py").by_id("nope") is None

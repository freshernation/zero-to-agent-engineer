"""Week 12, Day 3 - explaining it out loud.

Run me:  pytest week-12/day-3 -v

These check your answers cover the ground and are the right length. Whether they
sound like a person is Friday's job.
"""

import re

import pytest
from concepts import CONCEPTS

MIN_WORDS = 60
MAX_WORDS = 140


def answer_for(source, concept_id):
    text = re.sub(r"<!--.*?-->", "", source("ANSWERS.md"), flags=re.S)
    marker = f"## {concept_id}"
    assert marker in text, f"ANSWERS.md has no '{marker}' section."
    return text.split(marker, 1)[1].split("\n## ")[0].strip()


class TestEveryConceptIsAnswered:
    @pytest.mark.parametrize("concept", CONCEPTS, ids=lambda c: c["id"])
    def test_answered(self, source, concept):
        answer = answer_for(source, concept["id"])
        assert answer, f"No answer for '{concept['question']}'"


class TestLength:
    @pytest.mark.parametrize("concept", CONCEPTS, ids=lambda c: c["id"])
    def test_about_thirty_seconds(self, source, concept):
        answer = answer_for(source, concept["id"])
        words = len(answer.split())
        assert words >= MIN_WORDS, (
            f"'{concept['id']}' is {words} words. Under {MIN_WORDS} is a "
            "definition rather than an explanation - there is no room for the "
            "concrete detail that proves you have done it."
        )
        assert words <= MAX_WORDS, (
            f"'{concept['id']}' is {words} words. Over {MAX_WORDS} is more than "
            "thirty seconds, and talking too long reads as not knowing what "
            "matters."
        )


class TestCoverage:
    @pytest.mark.parametrize("concept", CONCEPTS, ids=lambda c: c["id"])
    def test_mentions_the_load_bearing_ideas(self, source, concept):
        answer = answer_for(source, concept["id"]).lower()
        missing = [
            " / ".join(options)
            for options in concept["must_mention"]
            if not any(option.lower() in answer for option in options)
        ]
        assert not missing, (
            f"'{concept['id']}' never mentions: {', '.join(missing)}.\n\n"
            f"Question: {concept['question']}\n\n"
            "These are not magic words - they are what somebody who understands "
            "the idea inevitably says. An answer without them is usually a "
            "definition that has been read rather than an explanation that is "
            "owned."
        )


class TestWrittenLikeSpeech:
    @pytest.mark.parametrize("concept", CONCEPTS, ids=lambda c: c["id"])
    def test_no_bullet_lists(self, source, concept):
        answer = answer_for(source, concept["id"])
        assert answer, f"No answer for '{concept['id']}' yet."
        bullets = [ln for ln in answer.splitlines() if ln.strip().startswith(("-", "*"))]
        assert len(bullets) <= 1, (
            f"'{concept['id']}' is a bulleted list. You cannot say bullets out "
            "loud - write down what you would actually say."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("ANSWERS.md")


class TestBank:
    def test_twelve_concepts(self):
        assert len(CONCEPTS) == 12

    def test_by_id(self, load):
        assert load("concepts.py").by_id("rag")["question"].startswith("What is RAG")
        assert load("concepts.py").by_id("nonsense") is None

    def test_questions(self, load):
        assert len(load("concepts.py").questions()) == 12

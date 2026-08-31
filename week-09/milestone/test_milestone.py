"""Week 9 milestone - RAG, measured.

Run me:  pytest week-09/milestone -v
"""

import re

import pytest
from chunking import fixed_chunks, sentence_chunks
from fake_model import FakeClient, text_reply
from golden import GOLDEN

REFUSAL = "I don't know based on the documents I have."


def fixed(size):
    return lambda text: fixed_chunks(text, size)


def sentences(size, overlap):
    return lambda text: sentence_chunks(text, size, overlap)


@pytest.fixture
def system(load, corpus_dir):
    return load("pipeline.py").RagSystem(sentences(400, 1)).build(corpus_dir)


class TestRagSystem:
    def test_build_returns_itself(self, load, corpus_dir):
        RagSystem = load("pipeline.py").RagSystem
        built = RagSystem(sentences(400, 1)).build(corpus_dir)
        assert built is not None and built.chunk_count > 6, (
            "build() should index the corpus and return self, so it can be chained."
        )

    def test_the_chunker_is_used(self, load, corpus_dir):
        RagSystem = load("pipeline.py").RagSystem
        small = RagSystem(fixed(150)).build(corpus_dir)
        large = RagSystem(fixed(600)).build(corpus_dir)
        assert small.chunk_count > large.chunk_count

    def test_search(self, system):
        results = system.search("when must expense claims be submitted")
        assert results[0]["chunk"]["source"] == "expenses.md"

    def test_k_is_respected(self, load, corpus_dir):
        RagSystem = load("pipeline.py").RagSystem
        assert len(RagSystem(sentences(400, 1), k=2).build(corpus_dir).search("claims")) == 2


class TestAnswer:
    def test_answers_a_real_question(self, system):
        client = FakeClient([text_reply("The fifth. [expenses.md#1]")])
        result = system.answer(client, "when must expense claims be submitted")
        assert result["refused"] is False
        assert result["answer"] == "The fifth. [expenses.md#1]"
        assert "expenses.md" in result["sources"]

    def test_the_context_reached_the_model(self, system):
        client = FakeClient([text_reply("ok")])
        system.answer(client, "when must expense claims be submitted")
        assert "fifth of the following month" in str(client.last_call["messages"])

    def test_refuses_without_calling_the_model(self, system):
        client = FakeClient([text_reply("I would invent something")])
        result = system.answer(client, "zzzzqqqq wwwwvvvv nonsense")
        assert result["refused"] is True
        assert result["answer"] == REFUSAL
        assert client.call_count == 0, (
            "The model was called with a context of noise. Check the top score "
            "first - refusing is a feature."
        )

    def test_refusing_returns_no_sources(self, system):
        client = FakeClient([text_reply("x")])
        assert system.answer(client, "zzzzqqqq wwwwvvvv")["sources"] == []

    def test_the_system_prompt_demands_citations(self, system):
        client = FakeClient([text_reply("ok")])
        system.answer(client, "when must expense claims be submitted")
        system_prompt = str(client.last_call.get("system", "")).lower()
        assert "cite" in system_prompt or "[" in system_prompt
        assert "only" in system_prompt

    def test_uses_temperature_zero(self, system):
        client = FakeClient([text_reply("ok")])
        system.answer(client, "when must expense claims be submitted")
        assert client.last_call.get("temperature") == 0


class TestHarness:
    def test_evaluate_shape(self, load, system):
        report = load("harness.py").evaluate(system, GOLDEN)
        assert set(report) == {"hit_rate", "hits", "total", "misses"}
        assert report["total"] == len(GOLDEN)
        assert report["hits"] + len(report["misses"]) == report["total"]

    def test_a_good_configuration_scores_well(self, load, system):
        rate = load("harness.py").evaluate(system, GOLDEN)["hit_rate"]
        assert 0.7 <= rate <= 1.0, f"Got {rate}."

    def test_compare(self, load, corpus_dir):
        RagSystem = load("pipeline.py").RagSystem
        reports = load("harness.py").compare(
            corpus_dir,
            GOLDEN,
            {
                "fixed-200": RagSystem(fixed(200)),
                "sentence-400-o1": RagSystem(sentences(400, 1)),
            },
        )
        assert set(reports) == {"fixed-200", "sentence-400-o1"}
        assert reports["sentence-400-o1"]["hit_rate"] > reports["fixed-200"]["hit_rate"], (
            f"Got {reports['fixed-200']['hit_rate']} and "
            f"{reports['sentence-400-o1']['hit_rate']}. The whole milestone rests "
            "on this difference being real and measurable."
        )

    def test_improvement(self, load, corpus_dir):
        mod = load("harness.py")
        RagSystem = load("pipeline.py").RagSystem
        reports = mod.compare(
            corpus_dir,
            GOLDEN,
            {
                "fixed-200": RagSystem(fixed(200)),
                "sentence-400-o1": RagSystem(sentences(400, 1)),
            },
        )
        delta = mod.improvement(reports, "fixed-200", "sentence-400-o1")
        assert delta > 0
        assert delta == round(delta, 3)

    def test_format_comparison(self, load, corpus_dir):
        mod = load("harness.py")
        RagSystem = load("pipeline.py").RagSystem
        reports = mod.compare(
            corpus_dir, GOLDEN, {"fixed-200": RagSystem(fixed(200))}
        )
        line = mod.format_comparison(reports).splitlines()[0]
        assert line.startswith("fixed-200")
        assert f"/{len(GOLDEN)}" in line, (
            f"Got {line!r}. Show the hits out of the total - a rate on its own "
            "hides how small the sample is."
        )

    def test_everything_is_scored_on_the_same_questions(self, load, corpus_dir):
        mod = load("harness.py")
        RagSystem = load("pipeline.py").RagSystem
        reports = mod.compare(
            corpus_dir,
            GOLDEN,
            {"a": RagSystem(fixed(200)), "b": RagSystem(sentences(400, 1))},
        )
        assert reports["a"]["total"] == reports["b"]["total"] == len(GOLDEN)


class TestReport:
    def test_prints_the_table(self, run):
        r = run("report.py")
        r.expect("RETRIEVAL EVALUATION")
        assert "/20" in r.stdout

    def test_prints_an_improvement(self, run):
        assert "Improvement:" in run("report.py").stdout

    def test_lists_the_remaining_misses(self, run):
        r = run("report.py")
        assert "Still missed" in r.stdout


class TestNoPrinting:
    @pytest.mark.parametrize("name,attribute", [
        ("pipeline.py", "RagSystem"), ("harness.py", "evaluate"),
    ])
    def test_libraries_stay_quiet(self, load, source, name, attribute):
        getattr(load(name), attribute)
        assert "print(" not in source(name, code_only=True), (
            f"{name} contains a print(). report.py does the displaying."
        )


class TestFindings:
    HEADINGS = [
        "What I measured",
        "The change",
        "What still fails",
        "What I would do next",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("FINDINGS.md")
        assert f"## {heading}" in text, f"FINDINGS.md has no '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, (
            f"'{heading}' is {len(body.split())} words."
        )

    def test_long_enough(self, source):
        assert len(self._body(source).split()) >= 350

    def test_has_numbers(self, source):
        numbers = re.findall(r"\d+\.?\d*", self._body(source))
        assert len(numbers) >= 2, (
            "FINDINGS.md needs at least two numbers in it. This document exists "
            "to replace 'it seemed to work' with a measurement."
        )

    def test_names_the_failure_mode(self, source):
        assert "retrieval miss" in self._body(source).lower(), (
            "Name the failure mode. 'It got it wrong' is not a diagnosis - "
            "which of the four was it?"
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("FINDINGS.md")

    def _body(self, source):
        text = re.sub(r"<!--.*?-->", "", source("FINDINGS.md"), flags=re.S)
        for heading in self.HEADINGS:
            text = text.replace(f"## {heading}", "")
        return text

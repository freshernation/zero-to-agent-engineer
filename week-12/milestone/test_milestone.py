"""Week 12 milestone - ten mocks, scored.

Run me:  pytest week-12/milestone -v
"""

import re

import pytest

DIMENSIONS = ("correctness", "structure", "specificity", "confidence")


class TestTheData:
    def test_ten_mocks(self, load):
        assert len(load("scores.py").MOCKS) == 10

    def test_numbered_one_to_ten(self, load):
        numbers = sorted(m["number"] for m in load("scores.py").MOCKS)
        assert numbers == list(range(1, 11))

    def test_every_gate_is_covered(self, load):
        gates = {m["gate"] for m in load("scores.py").MOCKS}
        assert gates == {1, 2, 3, 4, 5}, (
            f"Gates covered: {sorted(gates)}. At least one of each - a candidate "
            "who only practises the round they enjoy fails a different one."
        )

    @pytest.mark.parametrize("dimension", DIMENSIONS)
    def test_scores_are_in_range(self, load, dimension):
        for mock in load("scores.py").MOCKS:
            score = mock[dimension]
            assert isinstance(score, int) and 1 <= score <= 5, (
                f"Mock {mock['number']} has {dimension}={score!r}."
            )

    def test_baseline_exists(self, load):
        baseline = load("scores.py").BASELINE
        for dimension in DIMENSIONS:
            assert 1 <= baseline[dimension] <= 5

    def test_the_log_is_honest(self, load):
        """A log where everything is a 5 has hidden the two things worth fixing."""
        mocks = load("scores.py").MOCKS
        all_scores = [m[d] for m in mocks for d in DIMENSIONS]
        assert min(all_scores) <= 3, (
            "Nothing scored 3 or below across ten interviews. Either these were "
            "not real or the scoring was kind - and a kind log hides exactly the "
            "things it exists to find."
        )


class TestArithmetic:
    def test_mean_of(self, load):
        mock = {"number": 1, "gate": 1, "correctness": 4, "structure": 3,
                "specificity": 2, "confidence": 3}
        assert load("scores.py").mean_of(mock) == 3.0

    def test_mean_of_rounds(self, load):
        mock = {"number": 1, "gate": 1, "correctness": 4, "structure": 4,
                "specificity": 4, "confidence": 3}
        assert load("scores.py").mean_of(mock) == 3.75

    def test_overall(self, load):
        mod = load("scores.py")
        value = mod.overall(mod.MOCKS)
        assert 1.0 <= value <= 5.0
        assert value == round(value, 2)

    def test_by_gate(self, load):
        mod = load("scores.py")
        per_gate = mod.by_gate(mod.MOCKS)
        assert set(per_gate) == {1, 2, 3, 4, 5}
        assert all(1.0 <= v <= 5.0 for v in per_gate.values())

    def test_weakest_dimension(self, load):
        mod = load("scores.py")
        assert mod.weakest_dimension(mod.MOCKS) in DIMENSIONS

    def test_weakest_dimension_is_actually_the_lowest(self, load):
        mod = load("scores.py")
        weakest = mod.weakest_dimension(mod.MOCKS)
        means = {
            d: sum(m[d] for m in mod.MOCKS) / len(mod.MOCKS) for d in DIMENSIONS
        }
        assert means[weakest] == min(means.values())

    def test_improvement(self, load):
        mod = load("scores.py")
        delta = mod.improvement(mod.BASELINE, mod.MOCKS)
        assert delta == round(delta, 2)

    def test_trend(self, load):
        mod = load("scores.py")
        first, last = mod.trend(mod.MOCKS)
        assert 1.0 <= first <= 5.0 and 1.0 <= last <= 5.0


class TestTheLog:
    def test_ten_entries(self, source):
        text = re.sub(r"<!--.*?-->", "", source("MOCK_LOG.md"), flags=re.S)
        entries = re.findall(r"^## Mock \d+", text, flags=re.M)
        assert len(entries) == 10, (
            f"Found {len(entries)} entries. One per mock."
        )

    def test_entries_are_written(self, source):
        text = re.sub(r"<!--.*?-->", "", source("MOCK_LOG.md"), flags=re.S)
        sections = re.split(r"^## Mock \d+", text, flags=re.M)[1:]
        thin = [i + 1 for i, s in enumerate(sections) if len(s.split()) < 50]
        assert not thin, (
            f"Mocks {thin} are under 50 words. The worst question and what a "
            "better answer was - that is the whole value of keeping a log."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("MOCK_LOG.md")


class TestProgress:
    HEADINGS = [
        "The baseline",
        "What the numbers say",
        "What actually changed",
        "What is still weak",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("PROGRESS.md")
        assert f"## {heading}" in text
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 50, f"'{heading}' is too short."

    def test_long_enough(self, source):
        assert len(self._body(source).split()) >= 350

    def test_has_the_numbers(self, source):
        section = self._body(source)
        numbers = re.findall(r"\d+\.?\d*", section)
        assert len(numbers) >= 4, (
            "Fewer than four numbers. The baseline, the overall, the "
            "improvement and the trend are all figures - the point of this "
            "document is that it is evidence rather than reassurance."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("PROGRESS.md")

    def _body(self, source):
        text = re.sub(r"<!--.*?-->", "", source("PROGRESS.md"), flags=re.S)
        for heading in self.HEADINGS:
            text = text.replace(f"## {heading}", "")
        return text

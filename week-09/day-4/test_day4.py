"""Week 9, Day 4 - measuring it.

Run me:  pytest week-09/day-4 -v
"""

import pytest
from golden import GOLDEN

PLACEHOLDER = "(your answer)"


def fixed(size):
    def chunker(text):
        from chunking import fixed_chunks
        return fixed_chunks(text, size)
    return chunker


def sentences(size, overlap):
    def chunker(text):
        from chunking import sentence_chunks
        return sentence_chunks(text, size, overlap)
    return chunker


class TestIsHit:
    def test_finds_the_phrase(self, load):
        results = [{"score": 0.5, "chunk": {"text": "must be in by the fifth of the following month"}}]
        assert load("evaluate.py").is_hit(results, "fifth of the following month") is True

    def test_ignores_case(self, load):
        results = [{"score": 0.5, "chunk": {"text": "By The Fifth Of The Following Month"}}]
        assert load("evaluate.py").is_hit(results, "fifth of the following month") is True, (
            "Compare case-insensitively. A metric that scores itself too harshly "
            "sends you optimising something that was never broken."
        )

    def test_misses_when_absent(self, load):
        results = [{"score": 0.5, "chunk": {"text": "something else entirely"}}]
        assert load("evaluate.py").is_hit(results, "fifth of the following") is False

    def test_no_results(self, load):
        assert load("evaluate.py").is_hit([], "anything") is False

    def test_checks_every_result(self, load):
        results = [
            {"score": 0.5, "chunk": {"text": "wrong"}},
            {"score": 0.4, "chunk": {"text": "the fifth of the following month"}},
        ]
        assert load("evaluate.py").is_hit(results, "fifth of the following month") is True


class TestBuildStore:
    def test_builds_something_searchable(self, load, corpus_dir):
        store = load("evaluate.py").build_store(corpus_dir, sentences(400, 1))
        assert len(store) > 6
        results = store.search("when are expense claims due", k=1)
        assert results[0]["chunk"]["source"] == "expenses.md"

    def test_the_chunker_matters(self, load, corpus_dir):
        mod = load("evaluate.py")
        small = mod.build_store(corpus_dir, fixed(150))
        large = mod.build_store(corpus_dir, fixed(600))
        assert len(small) > len(large)


class TestHitRate:
    def test_sentence_chunking_scores_well(self, load, corpus_dir):
        mod = load("evaluate.py")
        store = mod.build_store(corpus_dir, sentences(400, 1))
        rate = mod.hit_rate(store, GOLDEN, k=3)
        assert 0.7 <= rate <= 1.0, (
            f"Got {rate}. Sentence chunking with overlap should score around "
            "0.85 on this corpus - well below that suggests a bug in is_hit or "
            "in the store."
        )

    def test_naive_chunking_scores_worse(self, load, corpus_dir):
        """The whole argument for measuring, in one assertion."""
        mod = load("evaluate.py")
        naive = mod.hit_rate(mod.build_store(corpus_dir, fixed(200)), GOLDEN, k=3)
        better = mod.hit_rate(
            mod.build_store(corpus_dir, sentences(400, 1)), GOLDEN, k=3
        )
        assert better > naive, (
            f"fixed-200 scored {naive} and sentence-400 scored {better}. The "
            "second should be higher - if it is not, the difference is in your "
            "chunking, and finding out why is the exercise."
        )

    def test_rounded(self, load, corpus_dir):
        mod = load("evaluate.py")
        rate = mod.hit_rate(mod.build_store(corpus_dir, sentences(400, 1)), GOLDEN)
        assert rate == round(rate, 3)

    def test_bigger_k_never_scores_worse(self, load, corpus_dir):
        mod = load("evaluate.py")
        store = mod.build_store(corpus_dir, sentences(400, 1))
        assert mod.hit_rate(store, GOLDEN, k=5) >= mod.hit_rate(store, GOLDEN, k=1)


class TestMisses:
    def test_lists_the_failures(self, load, corpus_dir):
        mod = load("evaluate.py")
        store = mod.build_store(corpus_dir, fixed(200))
        failures = mod.misses(store, GOLDEN, k=3)
        assert failures, "fixed-200 chunking should miss several of these."
        assert all(isinstance(f, str) for f in failures), (
            "misses() returns the questions themselves - the list is what tells "
            "you WHY, and the number only tells you whether."
        )

    def test_misses_agrees_with_hit_rate(self, load, corpus_dir):
        mod = load("evaluate.py")
        store = mod.build_store(corpus_dir, fixed(200))
        rate = mod.hit_rate(store, GOLDEN, k=3)
        failures = mod.misses(store, GOLDEN, k=3)
        assert len(failures) == round((1 - rate) * len(GOLDEN))


class TestEvaluate:
    def test_report_shape(self, load, corpus_dir):
        mod = load("evaluate.py")
        report = mod.evaluate(
            mod.build_store(corpus_dir, sentences(400, 1)), GOLDEN, k=3
        )
        assert set(report) == {"hit_rate", "hits", "total", "misses"}
        assert report["total"] == len(GOLDEN)
        assert report["hits"] + len(report["misses"]) == report["total"]


class TestCompareChunkers:
    def test_compares_several(self, load, corpus_dir):
        mod = load("evaluate.py")
        scores = mod.compare_chunkers(
            corpus_dir,
            GOLDEN,
            {
                "fixed-200": fixed(200),
                "fixed-400": fixed(400),
                "sentence-400": sentences(400, 1),
            },
            k=3,
        )
        assert set(scores) == {"fixed-200", "fixed-400", "sentence-400"}
        assert scores["sentence-400"] > scores["fixed-200"], (
            f"Got {scores}. This comparison is the deliverable of the week - "
            "one variable changed, both numbers, same questions."
        )


class TestFixes:
    def test_broken_1_compares_case_insensitively(self, run):
        run("broken_1.py").expect("Hit rate: 0.5")

    def test_broken_2_rebuilds_over_everything(self, run):
        run("broken_2.py").expect("Chunks: 6")

    def test_broken_3_indexes_everything(self, run, source):
        run("broken_3.py").expect("Top source: expenses.md")
        code = source("broken_3.py", code_only=True)
        assert "chunks[:4]" not in code.replace(" ", ""), (
            "Only four chunks were ever indexed, so the answer was not in the "
            "store to be found. That is a retrieval miss, and no prompt could "
            "have rescued it."
        )


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
        assert len(body.split()) >= 40, (
            f"The broken_{n}.py entry is too short. Answer all four prompts."
        )

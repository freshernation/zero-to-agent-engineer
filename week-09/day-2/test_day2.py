"""Week 9, Day 2 - vectors and a store.

Run me:  pytest week-09/day-2 -v
"""

import pytest

CHUNKS = [
    {"source": "expenses.md", "index": 0,
     "text": "Claims are submitted monthly and must be in by the fifth of the "
             "following month."},
    {"source": "expenses.md", "index": 1,
     "text": "Receipts are required for everything over ten pounds."},
    {"source": "oncall.md", "index": 0,
     "text": "The on-call rotation is one week long and runs from Wednesday "
             "morning to Wednesday morning."},
    {"source": "deployment.md", "index": 0,
     "text": "Deployments are blocked on Fridays after two in the afternoon."},
]


@pytest.fixture
def stocked(load):
    store = load("store.py").VectorStore()
    store.add(CHUNKS)
    return store


class TestStore:
    def test_starts_empty(self, load):
        store = load("store.py").VectorStore()
        assert len(store) == 0
        assert store.search("anything") == [], (
            "Searching an empty store should give nothing back, not raise."
        )

    def test_holds_the_chunks(self, stocked):
        assert len(stocked) == 4

    def test_sources(self, stocked):
        assert stocked.sources() == ["deployment.md", "expenses.md", "oncall.md"]

    def test_finds_the_right_chunk(self, stocked):
        results = stocked.search("when are expense claims due", k=1)
        assert results[0]["chunk"]["source"] == "expenses.md"
        assert "fifth" in results[0]["chunk"]["text"]

    def test_finds_a_different_right_chunk(self, stocked):
        results = stocked.search("how long is the on-call rotation", k=1)
        assert results[0]["chunk"]["source"] == "oncall.md"

    def test_results_are_sorted(self, stocked):
        results = stocked.search("expense claims", k=4)
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_k_limits_the_results(self, stocked):
        assert len(stocked.search("claims", k=2)) == 2
        assert len(stocked.search("claims", k=99)) == 4

    def test_result_shape(self, stocked):
        result = stocked.search("claims", k=1)[0]
        assert set(result) == {"score", "chunk"}
        assert isinstance(result["score"], float)

    def test_a_query_with_nothing_in_common(self, stocked):
        results = stocked.search("zzzz qqqq", k=3)
        assert all(r["score"] == 0.0 for r in results), (
            "No shared words at all should score zero. (In a neural embedding "
            "this effectively never happens - worth knowing.)"
        )

    def test_search_in_one_document(self, stocked):
        results = stocked.search_in("anything at all", "expenses.md", k=3)
        assert results, "Filtering to a source that exists should return something."
        assert all(r["chunk"]["source"] == "expenses.md" for r in results)

    def test_search_in_a_missing_document(self, stocked):
        assert stocked.search_in("claims", "nothing.md", k=3) == []

    def test_adding_twice_keeps_both(self, load):
        store = load("store.py").VectorStore()
        store.add(CHUNKS[:2])
        store.add(CHUNKS[2:])
        assert len(store) == 4, (
            "The second add replaced the first. Extend the collection."
        )

    def test_adding_twice_rebuilds_the_index(self, load):
        """idf depends on the whole collection - it cannot be computed once."""
        store = load("store.py").VectorStore()
        store.add(CHUNKS[:2])
        store.add(CHUNKS[2:])
        results = store.search("how long is the on-call rotation", k=1)
        assert results[0]["chunk"]["source"] == "oncall.md", (
            "Chunks added second are not searchable, or are scored against a "
            "stale idf. Rebuild the index whenever the collection changes."
        )


class TestAnalysis:
    @pytest.fixture
    def results(self, stocked):
        return stocked.search("expense claims submitted monthly", k=3)

    def test_best_source(self, load, results):
        assert load("analysis.py").best_source(results) == "expenses.md"

    def test_best_source_of_nothing(self, load):
        assert load("analysis.py").best_source([]) is None

    def test_source_counts(self, load, results):
        counts = load("analysis.py").source_counts(results)
        assert counts["expenses.md"] >= 1
        assert sum(counts.values()) == len(results)

    def test_score_gap(self, load):
        results = [{"score": 0.5, "chunk": {}}, {"score": 0.2, "chunk": {}}]
        assert load("analysis.py").score_gap(results) == 0.3

    def test_score_gap_with_one_result(self, load):
        assert load("analysis.py").score_gap([{"score": 0.5, "chunk": {}}]) == 0.0

    def test_score_gap_of_nothing(self, load):
        assert load("analysis.py").score_gap([]) == 0.0

    def test_looks_uncertain(self, load):
        mod = load("analysis.py")
        close = [{"score": 0.50, "chunk": {}}, {"score": 0.49, "chunk": {}}]
        clear = [{"score": 0.50, "chunk": {}}, {"score": 0.10, "chunk": {}}]
        assert mod.looks_uncertain(close) is True
        assert mod.looks_uncertain(clear) is False

    def test_format_results(self, load, results):
        lines = load("analysis.py").format_results(results).splitlines()
        assert len(lines) == len(results)
        assert "expenses.md#" in lines[0], (
            f"Got {lines[0]!r}. Include the source and the chunk index - that is "
            "what makes a citation checkable."
        )

    def test_format_results_truncates(self, load):
        long_chunk = {
            "source": "x.md", "index": 0, "text": "y" * 500,
        }
        line = load("analysis.py").format_results(
            [{"score": 0.5, "chunk": long_chunk}]
        )
        assert len(line) < 120, "Cut the text to 60 characters."

"""Week 7, Day 4 - concurrency and agent bugs.

Run me:  pytest week-07/day-4 -v
"""

import time

import pytest

PLACEHOLDER = "(your answer)"

THREE_SLOW = [
    ("t1", "slow_lookup", {"key": "alpha"}),
    ("t2", "slow_lookup", {"key": "beta"}),
    ("t3", "slow_lookup", {"key": "gamma"}),
]


class TestRunAll:
    def test_results_and_order(self, load):
        results = load("parallel.py").run_all(THREE_SLOW)
        assert results == [
            ("t1", "the first letter"),
            ("t2", "the second letter"),
            ("t3", "the third letter"),
        ], (
            f"Got {results}. gather preserves the order you passed things in - "
            "the ids have to line up with the right results."
        )

    def test_mixed_tools(self, load):
        results = load("parallel.py").run_all([
            ("a", "calculate", {"expression": "2+2"}),
            ("b", "word_count", {"text": "one two three"}),
        ])
        assert results == [("a", "4"), ("b", "3")]

    def test_unknown_tool_still_returns_a_result(self, load):
        results = load("parallel.py").run_all([("x", "nonsense", {})])
        assert len(results) == 1
        assert "Unknown tool" in results[0][1]

    def test_nothing_to_do(self, load):
        assert load("parallel.py").run_all([]) == []

    def test_it_is_actually_concurrent(self, load):
        """Three tools that each sleep 0.1s. Sequentially that is 0.3."""
        started = time.perf_counter()
        load("parallel.py").run_all(THREE_SLOW)
        elapsed = time.perf_counter() - started
        assert elapsed < 0.25, (
            f"Three concurrent 0.1s tools took {elapsed:.2f}s, so they ran one "
            "after another. Use asyncio.gather, and asyncio.to_thread for the "
            "blocking functions - awaiting them directly blocks the loop and "
            "gains you nothing."
        )

    def test_sequential_version_is_slower(self, load):
        started = time.perf_counter()
        load("parallel.py").run_all_sequential(THREE_SLOW)
        elapsed = time.perf_counter() - started
        assert elapsed >= 0.25, (
            "run_all_sequential is meant to be the slow one, for comparison."
        )


class TestAsyncPieces:
    def test_run_tool_async_is_a_coroutine(self, load):
        import asyncio
        import inspect

        function = load("parallel.py").run_tool_async
        assert inspect.iscoroutinefunction(function), (
            "run_tool_async should be an `async def`."
        )
        assert asyncio.run(function("calculate", {"expression": "2+2"})) == "4"

    def test_run_all_async_is_a_coroutine(self, load):
        import inspect

        assert inspect.iscoroutinefunction(load("parallel.py").run_all_async)


class TestFixes:
    def test_broken_1_resends_the_assistant_turn(self, run, source):
        run("broken_1.py").expect("Answer: It is 391.")
        code = source("broken_1.py", code_only=True)
        assert "assistant_turn" in code or '"assistant"' in code, (
            "The model's own turn has to go back into the history before the "
            "results do."
        )

    def test_broken_2_decides_what_to_do_at_the_cap(self, run):
        r = run("broken_2.py")
        r.expect("Answer: Stopped after 3 steps without finishing.")
        assert "Answer: None" not in r.stdout, (
            "The loop still falls off the end and returns None. A function that "
            "runs out of options has to say so."
        )

    def test_broken_3_matches_ids(self, run, source):
        run("broken_3.py").expect("Results: ['4', '2']")
        code = source("broken_3.py", code_only=True)
        assert '"tool_use_id": "t1"' not in code.replace("'", '"'), (
            "The id is still hard-coded. It has to come from the block being "
            "answered - it is the only thing linking an answer to its question."
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

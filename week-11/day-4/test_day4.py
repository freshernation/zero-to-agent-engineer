"""Week 11, Day 4 - workers in parallel, and who may hold what.

Run me:  pytest week-11/day-4 -v
"""

import asyncio
import inspect
import time

import pytest
from fake_model import FakeClient, ModelError, text_reply, tool_reply
from worker import make_worker

SLOW_SCHEMA = {
    "name": "slow_lookup",
    "description": "Looks something up, slowly. Takes a tenth of a second.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "The city"}},
        "required": ["city"],
    },
}


def slow_lookup(city):
    time.sleep(0.1)
    return f"{city}: found"


def slow_worker(name, city):
    client = FakeClient([
        tool_reply("slow_lookup", {"city": city}, id="t1"),
        text_reply(f"{city} done"),
    ])
    return make_worker(
        name, "Looks things up.", "You look things up.",
        [SLOW_SCHEMA], {"slow_lookup": slow_lookup}, client,
    )


def three_jobs():
    return [
        (slow_worker("first", "Lisbon"), "Lisbon"),
        (slow_worker("second", "Lagos"), "Lagos"),
        (slow_worker("third", "Bogota"), "Bogota"),
    ]


def broken_worker(name):
    return make_worker(
        name, "Fails.", "You fail.", [], {}, FakeClient([ModelError("overloaded")])
    )


class TestParallel:
    def test_returns_the_reports(self, load):
        assert load("fanout.py").run_parallel(three_jobs()) == [
            "Lisbon done", "Lagos done", "Bogota done"
        ]

    def test_keeps_the_order_of_the_jobs(self, load):
        jobs = list(reversed(three_jobs()))
        assert load("fanout.py").run_parallel(jobs) == [
            "Bogota done", "Lagos done", "Lisbon done"
        ]

    def test_runs_them_at_once(self, load):
        jobs = three_jobs()
        started = time.perf_counter()
        load("fanout.py").run_parallel(jobs)
        elapsed = time.perf_counter() - started
        assert elapsed < 0.25, (
            f"Three workers with a 0.1s tool each took {elapsed:.2f}s, so they "
            "ran one after another. Use asyncio.gather, with asyncio.to_thread "
            "around run_worker - it blocks, and awaiting it directly gains "
            "nothing."
        )

    def test_the_sequential_version_is_slower(self, load):
        jobs = three_jobs()
        started = time.perf_counter()
        reports = load("fanout.py").run_sequential(jobs)
        elapsed = time.perf_counter() - started
        assert reports == ["Lisbon done", "Lagos done", "Bogota done"]
        assert elapsed >= 0.25, (
            "run_sequential is meant to be the slow one, for comparison."
        )

    def test_each_worker_got_its_own_brief(self, load):
        jobs = three_jobs()
        load("fanout.py").run_parallel(jobs)
        for worker, brief in jobs:
            assert worker["client"].calls[0]["messages"][0]["content"] == brief

    def test_no_jobs(self, load):
        assert load("fanout.py").run_parallel([]) == []

    def test_the_async_piece_is_a_coroutine(self, load):
        function = load("fanout.py").run_parallel_async
        assert inspect.iscoroutinefunction(function), (
            "run_parallel_async should be an `async def`."
        )
        assert asyncio.run(function(three_jobs()[:1])) == ["Lisbon done"]


class TestOneFailureDoesNotLoseTheRest:
    def jobs(self):
        good = three_jobs()
        return [good[0], (broken_worker("flaky"), "anything"), good[2]]

    def test_the_others_still_report(self, load):
        reports = load("fanout.py").run_parallel(self.jobs())
        assert reports[0] == "Lisbon done"
        assert reports[2] == "Bogota done", (
            "One worker's model was down and the whole batch was lost. Each "
            "job has to fail on its own."
        )

    def test_the_failure_is_reported_in_its_place(self, load):
        reports = load("fanout.py").run_parallel(self.jobs())
        assert reports[1].startswith("Worker flaky failed:")
        assert "overloaded" in reports[1]

    def test_sequential_survives_a_failure_too(self, load):
        reports = load("fanout.py").run_sequential(self.jobs())
        assert reports[1].startswith("Worker flaky failed:")
        assert reports[2] == "Bogota done"

    def test_a_worker_that_does_not_finish(self, load):
        stuck = make_worker(
            "stuck", "Loops.", "You loop.", [SLOW_SCHEMA], {"slow_lookup": lambda city: "x"},
            FakeClient(tool_reply("slow_lookup", {"city": "x"})),
        )
        reports = load("fanout.py").run_parallel([(stuck, "go")])
        assert reports[0].startswith("Worker stuck did not finish")


def holder(name, tools, reads_untrusted=None):
    worker = make_worker(
        name, "x", "x", [], {tool: (lambda **kwargs: "ok") for tool in tools}, FakeClient()
    )
    if reads_untrusted is not None:
        worker["reads_untrusted"] = reads_untrusted
    return worker


DANGEROUS = {"send_email", "delete_file"}


class TestViolations:
    def test_a_reader_with_a_dangerous_tool(self, load):
        team = [holder("reader", ["fetch_page", "send_email"], reads_untrusted=True)]
        assert load("fanout.py").violations(team, DANGEROUS) == ["reader"], (
            "This worker reads pages a stranger wrote and can send email. One "
            "sentence on one page is all it takes."
        )

    def test_splitting_them_is_the_fix(self, load):
        team = [
            holder("reader", ["fetch_page"], reads_untrusted=True),
            holder("sender", ["send_email"], reads_untrusted=False),
        ]
        assert load("fanout.py").violations(team, DANGEROUS) == []

    def test_a_missing_flag_means_it_does_not_read_untrusted_text(self, load):
        team = [holder("sender", ["send_email"])]
        assert load("fanout.py").violations(team, DANGEROUS) == []

    def test_a_reader_with_safe_tools_is_fine(self, load):
        team = [holder("reader", ["fetch_page", "calculate"], reads_untrusted=True)]
        assert load("fanout.py").violations(team, DANGEROUS) == []

    def test_names_come_back_sorted(self, load):
        team = [
            holder("zed", ["delete_file"], reads_untrusted=True),
            holder("alpha", ["send_email"], reads_untrusted=True),
            holder("mid", ["fetch_page"], reads_untrusted=True),
        ]
        assert load("fanout.py").violations(team, DANGEROUS) == ["alpha", "zed"]

    def test_no_workers(self, load):
        assert load("fanout.py").violations([], DANGEROUS) == []

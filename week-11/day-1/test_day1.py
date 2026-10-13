"""Week 11, Day 1 - a worker is a function.

Run me:  pytest week-11/day-1 -v
"""

import pytest
from agent_kit import CALCULATE_SCHEMA, LOOKUP_SCHEMA, calculate, lookup_population
from fake_model import FakeClient, text_reply, tool_reply

DESCRIPTION = (
    "Finds population figures for cities. Give it the cities and say what "
    "form you want the numbers in."
)
SYSTEM = "You look up population figures. Report the number and the city."


def researcher(load, client):
    return load("worker.py").make_worker(
        "researcher", DESCRIPTION, SYSTEM,
        [LOOKUP_SCHEMA], {"lookup_population": lookup_population}, client,
    )


class TestMakeWorker:
    def test_holds_what_it_was_given(self, load):
        client = FakeClient()
        worker = researcher(load, client)
        assert worker["name"] == "researcher"
        assert worker["description"] == DESCRIPTION
        assert worker["system"] == SYSTEM
        assert worker["schemas"] == [LOOKUP_SCHEMA]
        assert worker["client"] is client
        assert set(worker["tools"]) == {"lookup_population"}


class TestWorkerSchema:
    def test_named_after_the_worker(self, load):
        schema = load("worker.py").worker_schema(researcher(load, FakeClient()))
        assert schema["name"] == "ask_researcher"

    def test_the_description_is_the_workers(self, load):
        schema = load("worker.py").worker_schema(researcher(load, FakeClient()))
        assert schema["description"] == DESCRIPTION, (
            "The orchestrator decides who to ask from this text alone. It is "
            "the worker's description, unchanged."
        )

    def test_takes_one_required_brief(self, load):
        schema = load("worker.py").worker_schema(researcher(load, FakeClient()))
        inputs = schema["input_schema"]
        assert inputs["type"] == "object"
        assert list(inputs["properties"]) == ["brief"]
        assert inputs["properties"]["brief"]["type"] == "string"
        assert inputs["required"] == ["brief"]

    def test_the_brief_is_described(self, load):
        schema = load("worker.py").worker_schema(researcher(load, FakeClient()))
        words = schema["input_schema"]["properties"]["brief"]["description"].split()
        assert len(words) >= 8, (
            "Describe the brief in a sentence. The model writing it has to be "
            "told the worker sees nothing else."
        )


class TestRunWorker:
    def test_returns_the_answer(self, load):
        client = FakeClient([text_reply("Lisbon has 545000 people.")])
        result = load("worker.py").run_worker(researcher(load, client), "Lisbon?")
        assert result["text"] == "Lisbon has 545000 people."
        assert result["stopped"] == "answered"
        assert result["worker"] == "researcher"

    def test_the_brief_is_all_it_gets(self, load):
        client = FakeClient([text_reply("ok")])
        load("worker.py").run_worker(researcher(load, client), "Population of Lisbon.")
        assert client.last_call["messages"] == [
            {"role": "user", "content": "Population of Lisbon."}
        ], (
            "The worker's conversation is one message: the brief. Nothing the "
            "orchestrator saw comes with it."
        )

    def test_uses_its_own_system_prompt(self, load):
        client = FakeClient([text_reply("ok")])
        load("worker.py").run_worker(researcher(load, client), "x")
        assert client.last_call["system"] == SYSTEM

    def test_is_offered_only_its_own_tools(self, load):
        client = FakeClient([text_reply("ok")])
        load("worker.py").run_worker(researcher(load, client), "x")
        assert [t["name"] for t in client.last_call["tools"]] == ["lookup_population"]

    def test_can_use_its_tools(self, load):
        client = FakeClient([
            tool_reply("lookup_population", {"city": "Lisbon"}, id="t1"),
            text_reply("545000"),
        ])
        result = load("worker.py").run_worker(researcher(load, client), "Lisbon?")
        assert result["tool_calls"][0]["result"] == "545000"
        assert result["steps"] == 2

    def test_cannot_use_a_tool_it_was_not_given(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "1+1"}, id="t1"),
            text_reply("I could not do that."),
        ])
        result = load("worker.py").run_worker(researcher(load, client), "1+1?")
        assert result["tool_calls"][0]["result"] == "Unknown tool: calculate", (
            "The researcher ran a tool that is not in its table. A worker's "
            "tools are the ones it was made with, and no others."
        )

    def test_starts_from_nothing_every_time(self, load):
        client = FakeClient([text_reply("first"), text_reply("second")])
        worker = researcher(load, client)
        mod = load("worker.py")
        mod.run_worker(worker, "Population of Lisbon.")
        mod.run_worker(worker, "And the one before?")
        assert len(client.calls[1]["messages"]) == 1, (
            "The second brief arrived with the first conversation attached. A "
            "worker remembers nothing between briefs - which is why the brief "
            "has to carry everything."
        )

    def test_max_steps_is_passed_on(self, load):
        client = FakeClient(tool_reply("lookup_population", {"city": "Lisbon"}))
        result = load("worker.py").run_worker(
            researcher(load, client), "Lisbon?", max_steps=2
        )
        assert result["stopped"] == "cap"
        assert client.call_count == 2


class TestReport:
    def test_an_answer_goes_back_as_it_is(self, load):
        result = {"worker": "researcher", "stopped": "answered", "text": "545000"}
        assert load("worker.py").report(result) == "545000"

    def test_a_worker_that_did_not_finish_says_so(self, load):
        result = {
            "worker": "researcher",
            "stopped": "cap",
            "text": "Stopped after 6 steps without finishing.",
        }
        assert load("worker.py").report(result) == (
            "Worker researcher did not finish: "
            "Stopped after 6 steps without finishing."
        ), (
            "Whoever asked has to be able to tell a finished answer from a "
            "worker that ran out of steps. Otherwise the cap message gets "
            "treated as the answer."
        )


class TestTwoWorkers:
    def test_each_has_its_own_model_and_tools(self, load):
        mod = load("worker.py")
        first = FakeClient([text_reply("545000")])
        second = FakeClient([text_reply("6")])
        research = researcher(load, first)
        analyst = mod.make_worker(
            "analyst", "Does arithmetic.", "You do arithmetic.",
            [CALCULATE_SCHEMA], {"calculate": calculate}, second,
        )
        mod.run_worker(research, "Lisbon?")
        mod.run_worker(analyst, "How many digits in 545000?")
        assert first.call_count == 1 and second.call_count == 1
        assert second.last_call["system"] == "You do arithmetic."
        assert mod.worker_schema(analyst)["name"] == "ask_analyst"

"""Week 11, Day 3 - the orchestrator.

Run me:  pytest week-11/day-3 -v

Every agent has its own scripted model, so you can see exactly who was asked
what, and in what order.
"""

import pytest
from agent_kit import CALCULATE_SCHEMA, LOOKUP_SCHEMA, calculate, lookup_population
from fake_model import FakeClient, ModelError, text_reply, tool_reply
from worker import make_worker

QUESTION = "How many people live in Lisbon and Bogota combined?"


def team(research_replies, analyst_replies):
    researcher = make_worker(
        "researcher", "Finds population figures for cities.",
        "You look up population figures.",
        [LOOKUP_SCHEMA], {"lookup_population": lookup_population},
        FakeClient(research_replies),
    )
    analyst = make_worker(
        "analyst", "Does arithmetic on numbers it is given.",
        "You do arithmetic.",
        [CALCULATE_SCHEMA], {"calculate": calculate},
        FakeClient(analyst_replies),
    )
    return researcher, analyst


def happy_path():
    """Ask the researcher, ask the analyst, answer."""
    researcher, analyst = team(
        [
            tool_reply("lookup_population", {"city": "Lisbon"}, id="r1"),
            tool_reply("lookup_population", {"city": "Bogota"}, id="r2"),
            text_reply("Lisbon 545000, Bogota 7900000."),
        ],
        [
            tool_reply("calculate", {"expression": "545000 + 7900000"}, id="a1"),
            text_reply("8445000"),
        ],
    )
    orchestrator = FakeClient([
        tool_reply("ask_researcher", {"brief": "Goal: populations of Lisbon and Bogota."}, id="d1"),
        tool_reply("ask_analyst", {"brief": "Goal: add 545000 and 7900000."}, id="d2"),
        text_reply("8,445,000 people."),
    ])
    return orchestrator, [researcher, analyst]


def tool_results(call):
    return [
        block["content"]
        for message in call["messages"]
        if isinstance(message.get("content"), list)
        for block in message["content"]
        if isinstance(block, dict) and block.get("type") == "tool_result"
    ]


class TestSystemPrompt:
    def test_tells_it_to_brief(self, load):
        system = load("team.py").ORCHESTRATOR_SYSTEM
        assert "brief" in system.lower()
        assert len(system.split()) >= 30


class TestRunTeam:
    def test_answers(self, load):
        orchestrator, workers = happy_path()
        result = load("team.py").run_team(orchestrator, QUESTION, workers)
        assert result["text"] == "8,445,000 people."
        assert result["stopped"] == "answered"

    def test_the_orchestrator_is_offered_only_workers(self, load):
        orchestrator, workers = happy_path()
        load("team.py").run_team(orchestrator, QUESTION, workers)
        offered = [tool["name"] for tool in orchestrator.calls[0]["tools"]]
        assert offered == ["ask_researcher", "ask_analyst"], (
            f"The orchestrator was offered {offered}. It holds no tools of its "
            "own - it can only ask."
        )

    def test_it_gets_the_users_question(self, load):
        orchestrator, workers = happy_path()
        load("team.py").run_team(orchestrator, QUESTION, workers)
        assert orchestrator.calls[0]["messages"][0]["content"] == QUESTION

    def test_the_worker_gets_the_brief_and_nothing_else(self, load):
        orchestrator, workers = happy_path()
        load("team.py").run_team(orchestrator, QUESTION, workers)
        first = workers[0]["client"].calls[0]["messages"]
        assert first == [
            {"role": "user", "content": "Goal: populations of Lisbon and Bogota."}
        ], (
            "The researcher should see the brief and only the brief - not the "
            "user's question, and not the orchestrator's conversation."
        )

    def test_the_report_goes_back_to_the_orchestrator(self, load):
        orchestrator, workers = happy_path()
        load("team.py").run_team(orchestrator, QUESTION, workers)
        assert tool_results(orchestrator.calls[1]) == ["Lisbon 545000, Bogota 7900000."]
        assert tool_results(orchestrator.calls[2])[-1] == "8445000"

    def test_the_orchestrator_never_sees_a_workers_tool_results(self, load):
        orchestrator, workers = happy_path()
        load("team.py").run_team(orchestrator, QUESTION, workers)
        everything = str(orchestrator.calls[-1]["messages"])
        assert "lookup_population" not in everything, (
            "The researcher's tool calls leaked into the orchestrator's "
            "context. Only the report crosses."
        )

    def test_delegations_are_recorded(self, load):
        orchestrator, workers = happy_path()
        result = load("team.py").run_team(orchestrator, QUESTION, workers)
        assert result["delegations"] == [
            {
                "worker": "researcher",
                "brief": "Goal: populations of Lisbon and Bogota.",
                "report": "Lisbon 545000, Bogota 7900000.",
            },
            {
                "worker": "analyst",
                "brief": "Goal: add 545000 and 7900000.",
                "report": "8445000",
            },
        ]

    def test_counts_every_model_call(self, load):
        orchestrator, workers = happy_path()
        result = load("team.py").run_team(orchestrator, QUESTION, workers)
        assert result["model_calls"] == {
            "orchestrator": 3, "researcher": 3, "analyst": 2
        }
        assert result["total_calls"] == 8, (
            "Eight model calls for a question one agent answers in four. That "
            "number is what the rest of the week is about."
        )

    def test_an_unused_worker_is_still_counted(self, load):
        researcher, analyst = team([text_reply("545000")], [])
        orchestrator = FakeClient([
            tool_reply("ask_researcher", {"brief": "Lisbon"}, id="d1"),
            text_reply("545000"),
        ])
        result = load("team.py").run_team(orchestrator, "Lisbon?", [researcher, analyst])
        assert result["model_calls"]["analyst"] == 0

    def test_no_delegation_at_all(self, load):
        researcher, analyst = team([], [])
        orchestrator = FakeClient([text_reply("Hello.")])
        result = load("team.py").run_team(orchestrator, "hi", [researcher, analyst])
        assert result["delegations"] == []
        assert result["total_calls"] == 1

    def test_asking_the_same_worker_twice_adds_up(self, load):
        researcher, analyst = team([text_reply("545000"), text_reply("7900000")], [])
        orchestrator = FakeClient([
            tool_reply("ask_researcher", {"brief": "Lisbon"}, id="d1"),
            tool_reply("ask_researcher", {"brief": "Bogota"}, id="d2"),
            text_reply("done"),
        ])
        result = load("team.py").run_team(orchestrator, "x", [researcher, analyst])
        assert result["model_calls"]["researcher"] == 2


class TestWhenAWorkerGoesWrong:
    def test_a_worker_that_does_not_finish(self, load):
        researcher, analyst = team(
            tool_reply("lookup_population", {"city": "Atlantis"}), []
        )
        orchestrator = FakeClient([
            tool_reply("ask_researcher", {"brief": "Atlantis"}, id="d1"),
            text_reply("I could not find that."),
        ])
        result = load("team.py").run_team(orchestrator, "Atlantis?", [researcher, analyst])
        assert result["delegations"][0]["report"].startswith(
            "Worker researcher did not finish"
        )
        assert result["text"] == "I could not find that."

    def test_a_worker_that_raises_does_not_take_the_team_down(self, load):
        researcher, analyst = team([ModelError("overloaded")], [])
        orchestrator = FakeClient([
            tool_reply("ask_researcher", {"brief": "Lisbon"}, id="d1"),
            text_reply("The researcher is unavailable."),
        ])
        result = load("team.py").run_team(orchestrator, "Lisbon?", [researcher, analyst])
        report = result["delegations"][0]["report"]
        assert report.startswith("Worker researcher failed:"), (
            f"The report was {report!r}. One worker's model being down is not "
            "a reason for the whole team to crash."
        )
        assert "overloaded" in report
        assert result["stopped"] == "answered"

    def test_the_failure_is_what_the_orchestrator_reads(self, load):
        researcher, analyst = team([ModelError("overloaded")], [])
        orchestrator = FakeClient([
            tool_reply("ask_researcher", {"brief": "Lisbon"}, id="d1"),
            text_reply("unavailable"),
        ])
        load("team.py").run_team(orchestrator, "Lisbon?", [researcher, analyst])
        assert "failed" in tool_results(orchestrator.calls[1])[0]


class TestLimits:
    def endless(self):
        researcher, analyst = team(text_reply("545000"), [])
        orchestrator = FakeClient(
            tool_reply("ask_researcher", {"brief": "Lisbon again"})
        )
        return orchestrator, researcher, analyst

    def test_delegation_limit(self, load):
        orchestrator, researcher, analyst = self.endless()
        result = load("team.py").run_team(
            orchestrator, "x", [researcher, analyst], max_delegations=2, max_steps=5
        )
        assert researcher["client"].call_count == 2, (
            f"The researcher ran {researcher['client'].call_count} times with a "
            "limit of 2. Past the limit the worker is not run at all."
        )
        assert result["delegations"][2]["report"] == (
            "Refused: delegation limit of 2 reached."
        )

    def test_refused_delegations_are_still_recorded(self, load):
        orchestrator, researcher, analyst = self.endless()
        result = load("team.py").run_team(
            orchestrator, "x", [researcher, analyst], max_delegations=2, max_steps=5
        )
        assert len(result["delegations"]) == 5

    def test_the_orchestrator_has_a_cap_of_its_own(self, load):
        orchestrator, researcher, analyst = self.endless()
        result = load("team.py").run_team(
            orchestrator, "x", [researcher, analyst], max_delegations=2, max_steps=3
        )
        assert result["stopped"] == "cap"
        assert result["model_calls"]["orchestrator"] == 3

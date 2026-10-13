"""Week 11 milestone - one agent or a team, measured.

Run me:  pytest week-11/milestone -v

Both designs run against scripted models here. Run them against a real one
yourself before you write the report - the numbers in it have to be yours.
"""

import re

import pytest
from fake_model import FakeClient, text_reply, tool_reply

QUESTION = "How many people live in Lisbon and Bogota combined?"


def single_script():
    return FakeClient([
        tool_reply("lookup_population", {"city": "Lisbon"}, id="s1"),
        tool_reply("lookup_population", {"city": "Bogota"}, id="s2"),
        tool_reply("calculate", {"expression": "545000 + 7900000"}, id="s3"),
        text_reply("8,445,000 people live in Lisbon and Bogota combined."),
    ])


def team_scripts():
    orchestrator = FakeClient([
        tool_reply("ask_researcher", {"brief": "Goal: populations of Lisbon and Bogota."}, id="d1"),
        tool_reply("ask_analyst", {"brief": "Goal: add 545000 and 7900000."}, id="d2"),
        text_reply("8,445,000 people."),
    ])
    researcher = FakeClient([
        tool_reply("lookup_population", {"city": "Lisbon"}, id="r1"),
        tool_reply("lookup_population", {"city": "Bogota"}, id="r2"),
        text_reply("Lisbon 545000, Bogota 7900000."),
    ])
    analyst = FakeClient([
        tool_reply("calculate", {"expression": "545000 + 7900000"}, id="a1"),
        text_reply("8445000"),
    ])
    return orchestrator, researcher, analyst


class TestSingle:
    def test_answers(self, load):
        result = load("designs.py").run_single(single_script(), QUESTION)
        assert "8,445,000" in result["text"]
        assert result["steps"] == 4

    def test_holds_both_tools(self, load):
        client = single_script()
        load("designs.py").run_single(client, QUESTION)
        assert {t["name"] for t in client.calls[0]["tools"]} == {
            "lookup_population", "calculate"
        }

    def test_has_a_system_prompt(self, load):
        client = single_script()
        load("designs.py").run_single(client, QUESTION)
        assert len(client.calls[0]["system"].split()) >= 10


class TestTeam:
    def test_two_workers_in_order(self, load):
        workers = load("designs.py").build_team(FakeClient(), FakeClient())
        assert [w["name"] for w in workers] == ["researcher", "analyst"]

    def test_each_holds_only_its_own_tool(self, load):
        researcher, analyst = load("designs.py").build_team(FakeClient(), FakeClient())
        assert set(researcher["tools"]) == {"lookup_population"}
        assert set(analyst["tools"]) == {"calculate"}, (
            "If the analyst can also look things up, you have built one agent "
            "twice. The split is the design."
        )
        assert [s["name"] for s in researcher["schemas"]] == ["lookup_population"]
        assert [s["name"] for s in analyst["schemas"]] == ["calculate"]

    def test_each_gets_its_own_client(self, load):
        first, second = FakeClient(), FakeClient()
        researcher, analyst = load("designs.py").build_team(first, second)
        assert researcher["client"] is first
        assert analyst["client"] is second

    def test_descriptions_an_orchestrator_can_choose_from(self, load):
        researcher, analyst = load("designs.py").build_team(FakeClient(), FakeClient())
        for worker in (researcher, analyst):
            assert len(worker["description"].split()) >= 10, (
                f"The {worker['name']}'s description is too short. It is the "
                "only thing the orchestrator has to go on."
            )
        assert researcher["description"] != analyst["description"]
        assert researcher["system"] != analyst["system"]

    def test_runs_as_a_team(self, load):
        mod = load("designs.py")
        orchestrator, research_client, analyst_client = team_scripts()
        workers = mod.build_team(research_client, analyst_client)
        result = mod.run_as_team(orchestrator, QUESTION, workers)
        assert result["text"] == "8,445,000 people."
        assert result["model_calls"] == {
            "orchestrator": 3, "researcher": 3, "analyst": 2
        }
        assert len(result["delegations"]) == 2


class TestPassed:
    def test_ignores_commas(self, load):
        passed = load("compare.py").passed
        assert passed("8,445,000 people.", "8445000") is True
        assert passed("8445000", "8,445,000") is True

    def test_a_wrong_number_fails(self, load):
        assert load("compare.py").passed("About 8 million.", "8445000") is False

    def test_ignores_capitals(self, load):
        assert load("compare.py").passed("YES, 14.5 times", "14.5") is True


RUNS_SINGLE = [
    {"passed": True, "model_calls": 4},
    {"passed": True, "model_calls": 2},
    {"passed": False, "model_calls": 4},
    {"passed": True, "model_calls": 3},
]
RUNS_TEAM = [
    {"passed": True, "model_calls": 8},
    {"passed": True, "model_calls": 5},
    {"passed": True, "model_calls": 8},
    {"passed": True, "model_calls": 6},
]


class TestSummarise:
    def test_a_summary(self, load):
        assert load("compare.py").summarise(RUNS_SINGLE) == {
            "tasks": 4, "pass_rate": 0.75, "calls_per_task": 3.2
        }

    def test_the_team(self, load):
        assert load("compare.py").summarise(RUNS_TEAM) == {
            "tasks": 4, "pass_rate": 1.0, "calls_per_task": 6.8
        }

    def test_no_runs(self, load):
        assert load("compare.py").summarise([]) == {
            "tasks": 0, "pass_rate": 0.0, "calls_per_task": 0.0
        }


class TestCompare:
    def test_gain_and_ratio(self, load):
        mod = load("compare.py")
        result = mod.compare(mod.summarise(RUNS_SINGLE), mod.summarise(RUNS_TEAM))
        assert result == {"quality_gain": 0.25, "cost_ratio": 2.1}

    def test_a_team_that_is_worse(self, load):
        mod = load("compare.py")
        result = mod.compare(mod.summarise(RUNS_TEAM), mod.summarise(RUNS_SINGLE))
        assert result["quality_gain"] == -0.25

    def test_no_calls_is_not_a_crash(self, load):
        mod = load("compare.py")
        result = mod.compare(mod.summarise([]), mod.summarise(RUNS_TEAM))
        assert result["cost_ratio"] == 0.0


class TestRecommend:
    def test_a_real_gain_earns_the_team(self, load):
        recommend = load("compare.py").recommend
        assert recommend({"quality_gain": 0.25, "cost_ratio": 2.1}) == "team"

    def test_no_gain_means_one_agent(self, load):
        recommend = load("compare.py").recommend
        assert recommend({"quality_gain": 0.0, "cost_ratio": 2.0}) == "single-agent", (
            "Twice the cost for the same answers. The dearer design has to buy "
            "something you can measure."
        )

    def test_a_small_gain_is_not_enough(self, load):
        recommend = load("compare.py").recommend
        assert recommend({"quality_gain": 0.05, "cost_ratio": 2.0}) == "single-agent"

    def test_exactly_the_margin_counts(self, load):
        recommend = load("compare.py").recommend
        assert recommend({"quality_gain": 0.10, "cost_ratio": 2.0}) == "team"

    def test_the_margin_can_be_changed(self, load):
        recommend = load("compare.py").recommend
        assert recommend({"quality_gain": 0.05, "cost_ratio": 2.0}, min_gain=0.05) == "team"


class TestHeadToHead:
    def test_the_whole_comparison(self, load):
        designs, compare = load("designs.py"), load("compare.py")

        single = designs.run_single(single_script(), QUESTION)
        orchestrator, research_client, analyst_client = team_scripts()
        team = designs.run_as_team(
            orchestrator, QUESTION,
            designs.build_team(research_client, analyst_client),
        )

        single_summary = compare.summarise([{
            "passed": compare.passed(single["text"], "8445000"),
            "model_calls": single["steps"],
        }])
        team_summary = compare.summarise([{
            "passed": compare.passed(team["text"], "8445000"),
            "model_calls": team["total_calls"],
        }])
        result = compare.compare(single_summary, team_summary)

        assert result == {"quality_gain": 0.0, "cost_ratio": 2.0}
        assert compare.recommend(result) == "single-agent"


class TestReport:
    HEADINGS = [
        "What I built",
        "The numbers",
        "What crossed the handoff",
        "Where a team would win",
        "My recommendation",
    ]

    def _body(self, source):
        text = source("REPORT.md")
        assert "<!--" not in text, "Delete the instructions comment."
        return text

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = self._body(source)
        assert f"## {heading}" in text, f"No '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, (
            f"'{heading}' is {len(body.split())} words."
        )

    def test_long_enough(self, source):
        assert len(self._body(source).split()) >= 350

    def test_has_numbers(self, source):
        assert len(re.findall(r"\d+\.?\d*", self._body(source))) >= 4, (
            "A measured comparison has numbers in it: pass rates, calls per "
            "task, the ratio."
        )

    def test_talks_about_the_brief(self, source):
        assert "brief" in self._body(source).lower(), (
            "Nothing about the brief. What you put in it, and what did not "
            "come back, is the part only you can report."
        )

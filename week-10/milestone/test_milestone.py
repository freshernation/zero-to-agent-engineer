"""Week 10 milestone - two designs, one recommendation.

Run me:  pytest week-10/milestone -v

The graph version runs against a scripted model. The crew is checked
structurally, because running it costs money.
"""

import re

import pytest
from fake_chat import FakeChat, ai, ai_tool

QUESTION = "What is the population of Lisbon, and how many digits is that?"


@pytest.fixture(autouse=True)
def dummy_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")


def two_step_script():
    return [
        ai_tool("city_info", {"city": "Lisbon"}, id="t1"),
        ai_tool("calculate", {"expression": "545000"}, id="t2"),
        ai("Lisbon has 545000 people, which is six digits."),
    ]


class TestGraphVersion:
    def test_answers(self, load):
        model = FakeChat(two_step_script())
        answer = load("graph_version.py").run(model, QUESTION)
        assert answer == "Lisbon has 545000 people, which is six digits."

    def test_takes_three_model_calls(self, load):
        model = FakeChat(two_step_script())
        _, calls = load("graph_version.py").run_with_steps(model, QUESTION)
        assert calls == 3, (
            f"Took {calls}. Two tools plus one to answer - that is the number "
            "the recommendation is built on, so it has to be right."
        )

    def test_a_single_tool_question(self, load):
        model = FakeChat([
            ai_tool("city_info", {"city": "Lisbon"}, id="t1"),
            ai("545000."),
        ])
        _, calls = load("graph_version.py").run_with_steps(model, "population?")
        assert calls == 2

    def test_binds_both_tools(self, load):
        model = FakeChat([ai("hi")])
        load("graph_version.py").run(model, "hi")
        names = {t.name for t in model.bound_tools}
        assert {"city_info", "calculate"} <= names, (
            "One agent with both tools is the design being compared. If it only "
            "has one tool it cannot do the task alone."
        )

    def test_the_cap(self, load):
        model = FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1"))
        assert load("graph_version.py").run(model, QUESTION, max_steps=4) == (
            "Stopped after 4 steps without finishing."
        )


class TestCrewVersion:
    def test_two_agents(self, load):
        crew = load("crew_version.py").build_crew()
        assert len(crew.agents) == 2
        assert len({a.role for a in crew.agents}) == 2

    def test_two_tasks_in_order(self, load):
        crew = load("crew_version.py").build_crew()
        assert len(crew.tasks) == 2
        assert "sequential" in str(crew.process).lower()

    def test_each_task_has_its_own_agent(self, load):
        crew = load("crew_version.py").build_crew()
        assert len({t.agent.role for t in crew.tasks}) == 2

    def test_agents_have_written_backstories(self, load):
        for agent in load("crew_version.py").build_crew().agents:
            assert len(agent.backstory.split()) >= 12

    def test_tasks_have_expected_outputs(self, load):
        for task in load("crew_version.py").build_crew().tasks:
            assert task.expected_output

    def test_describe(self, load):
        mod = load("crew_version.py")
        described = mod.describe(mod.build_crew())
        assert "2 agents" in described and "2 tasks" in described

    def test_no_kickoff(self, load, source):
        load("crew_version.py").build_crew
        assert "kickoff" not in source("crew_version.py", code_only=True), (
            "kickoff() makes real model calls. Run it by hand, not from a module "
            "the tests import."
        )


class TestAnalysis:
    def test_designs_named(self, load):
        assert set(load("analysis.py").DESIGNS) == {"single-agent", "crew"}

    def test_estimate(self, load):
        assert load("analysis.py").estimate(
            {"agent_count": 1, "tools_used": 2}
        ) == 3

    def test_compare(self, load):
        estimates = load("analysis.py").compare()
        assert set(estimates) == {"single-agent", "crew"}
        assert estimates["crew"] > estimates["single-agent"], (
            "A crew doing the same work in fewer calls than one agent would be "
            "a surprising result. Check the counts."
        )

    def test_ratio(self, load):
        ratio = load("analysis.py").ratio()
        assert ratio > 1.0
        assert ratio == round(ratio, 1)

    def test_recommend(self, load):
        assert load("analysis.py").recommend() in {"single-agent", "crew"}


class TestRecommendation:
    HEADINGS = [
        "The task",
        "The two designs",
        "What each costs",
        "Where the crew would win",
        "My recommendation",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("RECOMMENDATION.md")
        assert f"## {heading}" in text, f"No '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, (
            f"'{heading}' is {len(body.split())} words."
        )

    def test_long_enough(self, source):
        assert len(self._body(source).split()) >= 400

    def test_has_numbers(self, source):
        assert len(re.findall(r"\d+\.?\d*", self._body(source))) >= 2, (
            "Put the estimates in. A recommendation without a number is a "
            "preference."
        )

    def test_mentions_context(self, source):
        assert "context" in self._body(source).lower(), (
            "The handoff between agents is a string - everything the first one "
            "saw is gone. That is the sharpest objection to a multi-agent "
            "design, and a recommendation that skips it was written from taste."
        )

    def test_is_fair_to_the_crew(self, source):
        body = self._body(source)
        section = body.split("Where the crew would win")[-1] if "Where the crew would win" in body else body
        assert len(section.split()) >= 40

    def test_instructions_removed(self, source):
        assert "<!--" not in source("RECOMMENDATION.md")

    def _body(self, source):
        text = re.sub(r"<!--.*?-->", "", source("RECOMMENDATION.md"), flags=re.S)
        for heading in self.HEADINGS:
            text = text.replace(f"## {heading}", "")
        return text

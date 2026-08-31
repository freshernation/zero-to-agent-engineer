"""Week 10, Day 3 - CrewAI.

Run me:  pytest week-10/day-3 -v

Building a crew needs no key; running one costs money. These tests check the
wiring - the roles, the tools, the tasks, the order - which is most of what
there is to get right.
"""

import pytest


@pytest.fixture(autouse=True)
def dummy_key(monkeypatch):
    """CrewAI wants a key present to construct an LLM. It is never called."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")


class TestTools:
    def test_calculate(self, load):
        assert load("crew_tools.py").calculate.run(expression="17 * 23") == "391"

    def test_calculate_returns_rather_than_raises(self, load):
        result = load("crew_tools.py").calculate.run(expression="__import__('os')")
        assert result == "Unsafe expression", (
            f"Got {result!r}. A CrewAI tool should hand the problem back as a "
            "string - an exception inside a crew is much harder to find than "
            "one in your own loop."
        )

    def test_city_info(self, load):
        mod = load("crew_tools.py")
        assert mod.city_info.run(city="Lisbon") == (
            "Lisbon is in Portugal, population 545000."
        )
        assert mod.city_info.run(city="Narnia") == "I don't know about Narnia."

    def test_word_count(self, load):
        assert load("crew_tools.py").word_count.run(text="one two three") == "3"

    def test_docstrings_are_real(self, load):
        mod = load("crew_tools.py")
        for name in ("calculate", "city_info", "word_count"):
            tool = getattr(mod, name)
            assert len(tool.description.split()) >= 6, (
                f"{name}'s description is thin. Same rule as every week since "
                "seven: the description is the only thing the model knows."
            )


class TestAgents:
    def test_researcher(self, load):
        agent = load("crew_setup.py").make_researcher()
        assert agent.role
        assert "city_info" in [t.name for t in agent.tools]

    def test_analyst(self, load):
        agent = load("crew_setup.py").make_analyst()
        names = {t.name for t in agent.tools}
        assert {"calculate", "word_count"} <= names

    @pytest.mark.parametrize("maker", ["make_researcher", "make_analyst"])
    def test_every_agent_has_the_three_fields(self, load, maker):
        agent = getattr(load("crew_setup.py"), maker)()
        assert agent.role and agent.goal and agent.backstory

    @pytest.mark.parametrize("maker", ["make_researcher", "make_analyst"])
    def test_backstories_are_written(self, load, maker):
        agent = getattr(load("crew_setup.py"), maker)()
        words = len(agent.backstory.split())
        assert words >= 12, (
            f"The backstory is {words} words. role, goal and backstory become "
            "the system prompt - a vague backstory is a vague system prompt, "
            "and you learned what those produce in week 6."
        )

    def test_the_two_agents_are_different(self, load):
        mod = load("crew_setup.py")
        assert mod.make_researcher().role != mod.make_analyst().role, (
            "Two agents with the same role is one agent with extra model calls."
        )


class TestTasks:
    def test_two_tasks(self, load):
        mod = load("crew_setup.py")
        tasks = mod.make_tasks(mod.make_researcher(), mod.make_analyst())
        assert len(tasks) == 2

    def test_every_task_has_an_expected_output(self, load):
        mod = load("crew_setup.py")
        for task in mod.make_tasks(mod.make_researcher(), mod.make_analyst()):
            assert task.expected_output, (
                "expected_output is week 6's output contract with a new name. "
                "It is what the next task receives."
            )

    def test_tasks_are_assigned_to_different_agents(self, load):
        mod = load("crew_setup.py")
        researcher, analyst = mod.make_researcher(), mod.make_analyst()
        tasks = mod.make_tasks(researcher, analyst)
        roles = [t.agent.role for t in tasks]
        assert len(set(roles)) == 2, (
            f"Both tasks went to {roles}. If one agent does everything there is "
            "no crew, only overhead."
        )

    def test_descriptions_are_written(self, load):
        mod = load("crew_setup.py")
        for task in mod.make_tasks(mod.make_researcher(), mod.make_analyst()):
            assert len(task.description.split()) >= 6


class TestCrew:
    def test_build_crew(self, load):
        crew = load("crew_setup.py").build_crew()
        assert len(crew.agents) == 2
        assert len(crew.tasks) == 2

    def test_sequential(self, load):
        crew = load("crew_setup.py").build_crew()
        assert "sequential" in str(crew.process).lower(), (
            "Use Process.sequential - tasks run in order, each result feeding "
            "the next."
        )

    def test_describe_crew(self, load):
        mod = load("crew_setup.py")
        description = mod.describe_crew(mod.build_crew())
        assert description.startswith("2 agents")
        assert "2 tasks" in description
        assert "sequential" in description

    def test_did_not_run_it(self, load, source):
        """kickoff() calls a real model. Not in a test."""
        load("crew_setup.py").build_crew
        code = source("crew_setup.py", code_only=True)
        assert "kickoff" not in code, (
            "kickoff() makes real model calls and costs real money. Run it by "
            "hand once if you have a key - not from a module the tests import."
        )

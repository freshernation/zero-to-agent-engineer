"""Week 7, Day 3 - when the agent misbehaves.

Run me:  pytest week-07/day-3 -v
"""

import pytest
from fake_model import FakeClient, text_reply, tool_reply
from toolkit import all_schemas

CALC_SCHEMA = next(s for s in all_schemas() if s["name"] == "calculate")


class TestSignatures:
    def test_argument_order_does_not_matter(self, load):
        mod = load("guards.py")
        assert mod.call_signature("t", {"a": 1, "b": 2}) == (
            mod.call_signature("t", {"b": 2, "a": 1})
        ), (
            "The same call written two ways produced two signatures. Sort the "
            "keys - otherwise repeat detection misses the repeats."
        )

    def test_different_calls_differ(self, load):
        mod = load("guards.py")
        assert mod.call_signature("t", {"a": 1}) != mod.call_signature("t", {"a": 2})
        assert mod.call_signature("t", {"a": 1}) != mod.call_signature("u", {"a": 1})

    def test_count_calls(self, load):
        mod = load("guards.py")
        seen = [
            mod.call_signature("calculate", {"expression": "2+2"}),
            mod.call_signature("city_info", {"city": "Lisbon"}),
            mod.call_signature("calculate", {"expression": "2+2"}),
        ]
        assert mod.count_calls(seen, "calculate", {"expression": "2+2"}) == 2
        assert mod.count_calls(seen, "calculate", {"expression": "3+3"}) == 0

    def test_is_repeating(self, load):
        mod = load("guards.py")
        one = [mod.call_signature("calculate", {"expression": "2+2"})]
        assert mod.is_repeating(one, "calculate", {"expression": "2+2"}, limit=2) is False
        two = one * 2
        assert mod.is_repeating(two, "calculate", {"expression": "2+2"}, limit=2) is True


class TestValidateArguments:
    def test_good_arguments(self, load):
        ok, message = load("guards.py").validate_arguments(
            CALC_SCHEMA, {"expression": "2+2"}
        )
        assert ok is True and message == ""

    def test_missing_required(self, load):
        ok, message = load("guards.py").validate_arguments(CALC_SCHEMA, {})
        assert ok is False
        assert message == "missing required argument: expression", (
            f"Got {message!r}. The model reads this and fixes its next attempt, "
            "so it has to name the argument."
        )

    def test_unexpected_argument(self, load):
        ok, message = load("guards.py").validate_arguments(
            CALC_SCHEMA, {"expression": "2+2", "extra": 1}
        )
        assert ok is False
        assert message == "unexpected argument: extra"

    def test_missing_is_reported_before_unexpected(self, load):
        ok, message = load("guards.py").validate_arguments(CALC_SCHEMA, {"expr": "2+2"})
        assert ok is False
        assert "missing required argument: expression" in message


class TestTruncate:
    def test_short_text_is_untouched(self, load):
        assert load("guards.py").truncate("short", 500) == "short"

    def test_long_text_is_cut_and_marked(self, load):
        result = load("guards.py").truncate("a" * 900, 500)
        assert result.endswith("... [truncated]")
        assert result.startswith("a" * 500)

    def test_exactly_at_the_limit(self, load):
        assert load("guards.py").truncate("a" * 500, 500) == "a" * 500


class TestAgentHappyPath:
    def test_plain_answer(self, load):
        agent = load("robust.py").Agent(FakeClient([text_reply("Paris.")]))
        assert agent.run("Capital?") == "Paris."
        assert agent.stop_reason == "answered"
        assert agent.model_calls == 1

    def test_one_tool_then_an_answer(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "17 * 23"}, id="t1"),
            text_reply("It is 391."),
        ])
        agent = load("robust.py").Agent(client)
        assert agent.run("17 * 23?") == "It is 391."
        assert agent.stop_reason == "answered"
        assert agent.trace[0]["result"] == "391"


class TestAgentSurvivesBadTools:
    def test_unknown_tool_does_not_stop_the_run(self, load):
        client = FakeClient([
            tool_reply("search_web", {"query": "x"}, id="t1"),
            text_reply("Sorry, I do not have that. Here is what I can say."),
        ])
        agent = load("robust.py").Agent(client)
        answer = agent.run("look it up")
        assert agent.stop_reason == "answered", (
            "The agent gave up when the model invented a tool. Send back "
            "'Unknown tool: ...' and let it recover - self-correction is the "
            "entire reason there is a loop."
        )
        assert "Unknown tool: search_web" in agent.trace[0]["result"]

    def test_a_tool_that_raises(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "rm -rf /"}, id="t1"),
            text_reply("I could not calculate that."),
        ])
        agent = load("robust.py").Agent(client)
        agent.run("do something bad")
        assert agent.stop_reason == "answered"
        assert "Tool failed" in agent.trace[0]["result"]

    def test_missing_arguments(self, load):
        client = FakeClient([
            tool_reply("calculate", {}, id="t1"),
            text_reply("Let me try again differently."),
        ])
        agent = load("robust.py").Agent(client)
        agent.run("calculate something")
        assert agent.stop_reason == "answered"
        result = agent.trace[0]["result"].lower()
        assert "expression" in result, (
            f"The result was {agent.trace[0]['result']!r}. Tell the model which "
            "argument was missing - a message it can act on is worth far more "
            "than one that just says something went wrong."
        )

    def test_results_are_truncated(self, load):
        client = FakeClient([
            tool_reply("word_count", {"text": "word " * 400}, id="t1"),
            text_reply("done"),
        ])
        agent = load("robust.py").Agent(client)
        agent.run("count them")
        assert len(agent.trace[0]["result"]) <= 520


class TestAgentStops:
    def test_repeat_detection(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "2+2"}, id="t1"))
        agent = load("robust.py").Agent(client, max_iterations=10, max_repeats=2)
        answer = agent.run("go in circles")
        assert agent.stop_reason == "looping", (
            f"stop_reason was {agent.stop_reason!r}. The same call twice is a "
            "loop - catching it in two steps instead of ten is most of the "
            "saving."
        )
        assert answer == "Stopped: the agent repeated the same tool call."
        assert agent.model_calls < 10

    def test_different_calls_are_not_a_loop(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "1+1"}, id="t1"),
            tool_reply("calculate", {"expression": "2+2"}, id="t2"),
            tool_reply("calculate", {"expression": "3+3"}, id="t3"),
            text_reply("All done."),
        ])
        agent = load("robust.py").Agent(client, max_repeats=2)
        assert agent.run("three sums") == "All done."
        assert agent.stop_reason == "answered"

    def test_the_cap_still_applies(self, load):
        """Repeats are ruled out here, so only the cap can stop it."""
        client = FakeClient([
            tool_reply("calculate", {"expression": f"{n}+{n}"}, id=f"t{n}")
            for n in range(20)
        ])
        agent = load("robust.py").Agent(client, max_iterations=4, max_repeats=3)
        assert agent.run("keep going") == "Stopped after 4 steps without finishing."
        assert agent.stop_reason == "cap"
        assert agent.model_calls == 4


class TestNoFrameworks:
    @pytest.mark.parametrize("name", ["guards.py", "robust.py"])
    def test_the_fence(self, load, source, name):
        load(name)
        code = source(name, code_only=True)
        assert code.strip(), (
            f"{name} has nothing in it yet - write it first."
        )
        code = code.lower()
        for banned in ("langchain", "langgraph", "crewai", "autogen"):
            assert banned not in code, f"{name} imports {banned}. Not this week."

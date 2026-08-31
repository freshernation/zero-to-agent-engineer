"""Week 8 milestone - both agents, and the comparison.

Run me:  pytest week-08/milestone -v

The two agents talk to different SDKs, so each gets its own scripted fake. Given
equivalent scripts they must behave identically - that equivalence is what makes
the comparison honest.
"""

import re

import pytest
from fake_chat import FakeChat, ai, ai_tool
from fake_model import FakeClient, text_reply, tool_reply


def anthropic_script():
    return [
        tool_reply("calculate", {"expression": "17 * 23"}, id="t1"),
        text_reply("It is 391."),
    ]


def langchain_script():
    return [
        ai_tool("calculate", {"expression": "17 * 23"}, id="t1"),
        ai("It is 391."),
    ]


class TestHandwritten:
    def test_plain_answer(self, load):
        client = FakeClient([text_reply("Paris.")])
        assert load("handwritten.py").run(client, "Capital?") == "Paris."

    def test_one_tool(self, load):
        client = FakeClient(anthropic_script())
        assert load("handwritten.py").run(client, "17 * 23?") == "It is 391."

    def test_steps(self, load):
        client = FakeClient(anthropic_script())
        _, steps = load("handwritten.py").run_with_steps(client, "17 * 23?")
        assert steps == 2

    def test_unknown_tool_carries_on(self, load):
        client = FakeClient([
            tool_reply("search_web", {"q": "x"}, id="t1"),
            text_reply("I do not have that."),
        ])
        assert load("handwritten.py").run(client, "x") == "I do not have that."

    def test_the_cap(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
        assert load("handwritten.py").run(client, "forever", max_steps=4) == (
            "Stopped after 4 steps without finishing."
        )


class TestGraphAgent:
    def test_plain_answer(self, load):
        model = FakeChat([ai("Paris.")])
        assert load("graph_agent.py").run(model, "Capital?") == "Paris."

    def test_one_tool(self, load):
        model = FakeChat(langchain_script())
        assert load("graph_agent.py").run(model, "17 * 23?") == "It is 391."

    def test_steps(self, load):
        model = FakeChat(langchain_script())
        _, steps = load("graph_agent.py").run_with_steps(model, "17 * 23?")
        assert steps == 2

    def test_unknown_tool_carries_on(self, load):
        model = FakeChat([
            ai_tool("search_web", {"q": "x"}, id="t1"),
            ai("I do not have that."),
        ])
        assert load("graph_agent.py").run(model, "x") == "I do not have that."

    def test_the_cap(self, load):
        model = FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1"))
        assert load("graph_agent.py").run(model, "forever", max_steps=4) == (
            "Stopped after 4 steps without finishing."
        )


class TestTheyAgree:
    """The basis of the whole comparison."""

    def test_same_answer_with_no_tools(self, load):
        mod = load("compare.py")
        assert mod.agree(
            FakeClient([text_reply("Paris.")]), FakeChat([ai("Paris.")]), "Capital?"
        )

    def test_same_answer_with_a_tool(self, load):
        mod = load("compare.py")
        handwritten, graph = mod.both_answers(
            FakeClient(anthropic_script()), FakeChat(langchain_script()), "17 * 23?"
        )
        assert handwritten == graph == "It is 391.", (
            f"handwritten said {handwritten!r}, graph said {graph!r}. Two agents "
            "that do not agree cannot be compared honestly - find the difference "
            "before writing a word of COMPARISON.md."
        )

    def test_same_number_of_model_calls(self, load):
        _, hand_steps = load("handwritten.py").run_with_steps(
            FakeClient(anthropic_script()), "17 * 23?"
        )
        _, graph_steps = load("graph_agent.py").run_with_steps(
            FakeChat(langchain_script()), "17 * 23?"
        )
        assert hand_steps == graph_steps

    def test_same_behaviour_at_the_cap(self, load):
        hand = load("handwritten.py").run(
            FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1")),
            "forever", max_steps=3,
        )
        graph = load("graph_agent.py").run(
            FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1")),
            "forever", max_steps=3,
        )
        assert hand == graph


class TestCompare:
    def test_count_lines_ignores_blanks_and_comments(self, load, tmp_path):
        path = tmp_path / "sample.py"
        path.write_text("# a comment\n\nx = 1\n\n# another\ny = 2\n")
        assert load("compare.py").count_lines(str(path)) == 2

    def test_line_counts(self, load):
        counts = load("compare.py").line_counts()
        assert set(counts) == {"handwritten", "graph"}
        assert all(isinstance(v, int) and v > 0 for v in counts.values()), (
            f"Got {counts}. These are the numbers that go in COMPARISON.md."
        )


class TestComparisonDocument:
    HEADINGS = [
        "What the framework removed",
        "What it did not",
        "Line counts",
        "Debugging",
        "What I would choose",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("COMPARISON.md")
        assert f"## {heading}" in text, f"COMPARISON.md has no '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, (
            f"'{heading}' is {len(body.split())} words. This document is the "
            "reason week 7 existed - it is worth an hour."
        )

    def test_long_enough(self, source):
        body = self._body(source)
        assert len(body.split()) >= 400, (
            f"COMPARISON.md is {len(body.split())} words of content, needs 400."
        )

    @pytest.mark.parametrize("idea", ["reducer", "conditional edge"])
    def test_names_what_the_framework_gave_you(self, source, idea):
        assert idea in self._body(source).lower(), (
            f"COMPARISON.md never mentions '{idea}'. Those are the two things "
            "LangGraph actually added - a comparison that misses them was "
            "written from impressions rather than from the code."
        )

    def test_contains_a_real_number(self, source):
        assert re.search(r"\d", self._body(source)), (
            "No numbers anywhere. Put the line counts in - a figure is worth "
            "more than an adjective."
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("COMPARISON.md"), (
            "The instructions comment is still there. Delete it."
        )

    def _body(self, source):
        text = re.sub(r"<!--.*?-->", "", source("COMPARISON.md"), flags=re.S)
        for heading in self.HEADINGS:
            text = text.replace(f"## {heading}", "")
        return text

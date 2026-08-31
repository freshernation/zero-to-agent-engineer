"""Week 8, Day 3 - the port.

Run me:  pytest week-08/day-3 -v
"""

import pytest
from fake_chat import FakeChat, ai, ai_tool, ai_tools
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def calc_then_answer(expression="17 * 23", answer="It is 391."):
    return [ai_tool("calculate", {"expression": expression}, id="t1"), ai(answer)]


class TestState:
    def test_messages_accumulate(self, load):
        """add_messages appends. Without a reducer each node would overwrite."""
        mod = load("agent_graph.py")
        model = FakeChat(calc_then_answer())
        _, state = mod.run_with_state(model, "17 * 23?")
        assert len(state["messages"]) >= 4, (
            f"Only {len(state['messages'])} messages survived. Expected the "
            "question, the tool request, the tool result and the answer."
        )

    def test_steps_are_counted(self, load):
        mod = load("agent_graph.py")
        _, state = mod.run_with_state(FakeChat(calc_then_answer()), "x")
        assert state["steps"] == 2


class TestRunTools:
    def test_one_call(self, load):
        mod = load("agent_graph.py")
        request = ai_tool("calculate", {"expression": "17 * 23"}, id="t1")
        update = mod.run_tools({"messages": [request], "steps": 1})
        results = update["messages"]
        assert len(results) == 1
        assert isinstance(results[0], ToolMessage)
        assert results[0].content == "391"
        assert results[0].tool_call_id == "t1", (
            "The tool_call_id has to match the request. Same rule as last "
            "week's tool_use_id, same bug if you get it wrong."
        )

    def test_several_calls(self, load):
        mod = load("agent_graph.py")
        request = ai_tools([
            ("calculate", {"expression": "2+2"}, "a"),
            ("word_count", {"text": "one two three"}, "b"),
        ])
        results = mod.run_tools({"messages": [request], "steps": 1})["messages"]
        assert [r.tool_call_id for r in results] == ["a", "b"]
        assert [r.content for r in results] == ["4", "3"]

    def test_unknown_tool(self, load):
        mod = load("agent_graph.py")
        request = ai_tool("search_web", {"q": "x"}, id="t1")
        results = mod.run_tools({"messages": [request], "steps": 1})["messages"]
        assert len(results) == 1, "One call in, one result out - always."
        assert "Unknown tool" in results[0].content

    def test_tool_that_raises(self, load):
        mod = load("agent_graph.py")
        request = ai_tool("calculate", {"expression": "rm -rf /"}, id="t1")
        results = mod.run_tools({"messages": [request], "steps": 1})["messages"]
        assert "Tool failed" in results[0].content, (
            "A tool that raises still owes the model an answer. The framework "
            "did not take this decision away from you."
        )


class TestRouting:
    def test_stops_when_there_are_no_tool_calls(self, load):
        from langgraph.graph import END

        route = load("agent_graph.py").make_route(6)
        state = {"messages": [AIMessage("Paris.")], "steps": 1}
        assert route(state) == END

    def test_goes_to_tools_when_asked(self, load):
        route = load("agent_graph.py").make_route(6)
        state = {"messages": [ai_tool("calculate", {"expression": "2+2"})], "steps": 1}
        assert route(state) == "tools"

    def test_the_cap_wins(self, load):
        from langgraph.graph import END

        route = load("agent_graph.py").make_route(3)
        state = {"messages": [ai_tool("calculate", {"expression": "2+2"})], "steps": 3}
        assert route(state) == END, (
            "The cap has to be checked before the tool_calls. LangGraph's own "
            "recursion_limit raises instead of ending cleanly, which is not what "
            "you want a customer to see."
        )


class TestRun:
    def test_plain_answer(self, load):
        assert load("agent_graph.py").run(FakeChat([ai("Paris.")]), "Capital?") == (
            "Paris."
        )

    def test_one_tool_then_an_answer(self, load):
        model = FakeChat(calc_then_answer())
        assert load("agent_graph.py").run(model, "17 * 23?") == "It is 391."

    def test_the_tool_actually_ran(self, load):
        model = FakeChat(calc_then_answer())
        mod = load("agent_graph.py")
        _, state = mod.run_with_state(model, "17 * 23?")
        results = [m for m in state["messages"] if isinstance(m, ToolMessage)]
        assert results and results[0].content == "391"

    def test_two_tools_in_sequence(self, load):
        model = FakeChat([
            ai_tool("calculate", {"expression": "2+2"}, id="t1"),
            ai_tool("city_info", {"city": "Lisbon"}, id="t2"),
            ai("Both done."),
        ])
        assert load("agent_graph.py").run(model, "two things") == "Both done."

    def test_tools_are_bound(self, load):
        model = FakeChat([ai("hi")])
        load("agent_graph.py").run(model, "hi")
        assert model.bound_tools, (
            "bind_tools was never called - the model cannot ask for a tool it "
            "was never told about."
        )

    def test_the_question_reaches_the_model(self, load):
        model = FakeChat([ai("hi")])
        load("agent_graph.py").run(model, "what is up")
        humans = [m for m in model.last_call if isinstance(m, HumanMessage)]
        assert humans, "No HumanMessage was sent at all."
        assert humans[0].content == "what is up", (
            f"The question arrived as {humans[0].content!r}. Put any standing "
            "instructions in a SystemMessage rather than gluing them onto the "
            "question - same separation as week 6's system field."
        )


class TestTheCap:
    def test_stops_and_says_so(self, load):
        model = FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1"))
        result = load("agent_graph.py").run(model, "forever", max_steps=4)
        assert model.call_count == 4, (
            f"The model was called {model.call_count} times with a cap of 4."
        )
        assert result == "Stopped after 4 steps without finishing.", (
            f"Got {result!r}. Running out of steps is an outcome - say so."
        )

    def test_the_graph_terminates_at_all(self, load):
        """Without a cap this test never finishes."""
        model = FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1"))
        load("agent_graph.py").run(model, "forever", max_steps=3)

    def test_a_lower_cap_calls_less(self, load):
        model = FakeChat(ai_tool("calculate", {"expression": "1+1"}, id="t1"))
        load("agent_graph.py").run(model, "forever", max_steps=2)
        assert model.call_count == 2


class TestNoShortcut:
    def test_did_not_call_the_prebuilt_agent(self, load, source):
        load("agent_graph.py").build_agent  # nothing to check until it exists
        code = source("agent_graph.py", code_only=True)
        assert "create_react_agent" not in code, (
            "create_react_agent builds this in four lines, and it is fenced off "
            "for a reason: comparing your loop to a function you called teaches "
            "nothing. Wire the graph yourself out of the same pieces."
        )

    def test_actually_used_a_graph(self, load, source):
        load("agent_graph.py")
        code = source("agent_graph.py", code_only=True)
        assert "StateGraph" in code, "Build a StateGraph - that is the exercise."
        assert "add_conditional_edges" in code, (
            "The decision between 'run the tools' and 'stop' is a conditional "
            "edge. That is the piece that replaces your if statement."
        )

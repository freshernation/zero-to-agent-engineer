"""Week 7, Day 2 - the loop.

Run me:  pytest week-07/day-2 -v
"""

import pytest
from fake_model import FakeClient, Message, TextBlock, ToolUseBlock, text_reply, tool_reply


def calc_then_answer(expression="17 * 23", answer="17 * 23 is 391."):
    return [
        tool_reply("calculate", {"expression": expression}, id="t1"),
        text_reply(answer),
    ]


class TestToolResultMessage:
    def test_shape(self, load):
        message = load("agent.py").tool_result_message([("t1", "391")])
        assert message["role"] == "user", (
            "A tool result goes back as a USER message. There is no special "
            "channel - you are telling the model what happened."
        )
        assert message["content"] == [
            {"type": "tool_result", "tool_use_id": "t1", "content": "391"}
        ]

    def test_several_results(self, load):
        message = load("agent.py").tool_result_message([("t1", "4"), ("t2", "2")])
        assert len(message["content"]) == 2
        assert [b["tool_use_id"] for b in message["content"]] == ["t1", "t2"]


class TestRun:
    def test_answers_without_tools(self, load):
        client = FakeClient([text_reply("Paris.")])
        assert load("agent.py").run(client, "Capital of France?") == "Paris."

    def test_one_tool_then_an_answer(self, load):
        client = FakeClient(calc_then_answer())
        assert load("agent.py").run(client, "What is 17 * 23?") == "17 * 23 is 391."

    def test_sends_the_tools(self, load):
        client = FakeClient([text_reply("hi")])
        load("agent.py").run(client, "hi")
        assert client.last_call.get("tools"), (
            "No tools= in the request. The model cannot ask for a tool it was "
            "never told about."
        )

    def test_the_tool_actually_ran(self, load):
        """The result the model sees must come from running the function."""
        client = FakeClient(calc_then_answer())
        load("agent.py").run(client, "What is 17 * 23?")
        second = client.calls[1]["messages"]
        results = [
            block
            for message in second
            if isinstance(message.get("content"), list)
            for block in message["content"]
            if isinstance(block, dict) and block.get("type") == "tool_result"
        ]
        assert results, "The second call carried no tool_result at all."
        assert results[0]["content"] == "391", (
            f"The tool result was {results[0]['content']!r}. It should be 391 - "
            "the value your own calculate() returned."
        )

    def test_resends_the_assistant_turn(self, load):
        client = FakeClient(calc_then_answer())
        load("agent.py").run(client, "What is 17 * 23?")
        roles = [m["role"] for m in client.calls[1]["messages"]]
        assert roles == ["user", "assistant", "user"], (
            f"The second call sent {roles}. You must resend what the model said, "
            "tool call included - otherwise it sees a result for a request it has "
            "no record of making."
        )

    def test_two_tools_in_sequence(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "2+2"}, id="t1"),
            tool_reply("city_info", {"city": "Lisbon"}, id="t2"),
            text_reply("Done."),
        ])
        assert load("agent.py").run(client, "two things") == "Done."

    def test_several_tools_in_one_response(self, load):
        client = FakeClient([
            Message(
                [
                    ToolUseBlock("calculate", {"expression": "2+2"}, "t1"),
                    ToolUseBlock("word_count", {"text": "a b c"}, "t2"),
                ],
                stop_reason="tool_use",
            ),
            text_reply("Both done."),
        ])
        assert load("agent.py").run(client, "two at once") == "Both done."
        results = client.calls[1]["messages"][-1]["content"]
        assert len(results) == 2, (
            "One response asked for two tools. Both have to run, and both "
            "results go back in the same user message."
        )


class TestTheCap:
    def test_stops_and_says_so(self, load):
        """A model that always asks for a tool would loop forever."""
        client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
        result = load("agent.py").run(client, "go forever", max_iterations=5)
        assert result == "Stopped after 5 steps without finishing.", (
            f"Got {result!r}. Without a cap this runs until you notice the bill."
        )

    def test_makes_exactly_that_many_calls(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
        load("agent.py").run(client, "go forever", max_iterations=3)
        assert client.call_count == 3

    def test_a_lower_cap(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
        assert load("agent.py").run(client, "x", max_iterations=2) == (
            "Stopped after 2 steps without finishing."
        )


class TestIterationsUsed:
    def test_one_when_it_just_answers(self, load):
        client = FakeClient([text_reply("Paris.")])
        assert load("agent.py").iterations_used(client, "x") == 1

    def test_two_for_one_tool_call(self, load):
        client = FakeClient(calc_then_answer())
        assert load("agent.py").iterations_used(client, "x") == 2

    def test_stops_at_the_cap(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
        assert load("agent.py").iterations_used(client, "x", max_iterations=4) == 4


class TestTrace:
    def test_answer_only(self, load):
        client = FakeClient([text_reply("Paris.")])
        final, trace = load("agent.py").run_with_trace(client, "x")
        assert final == "Paris."
        assert len(trace) == 1
        assert trace[0]["type"] == "answer"
        assert trace[0]["text"] == "Paris."
        assert trace[0]["step"] == 1

    def test_records_the_tool_call(self, load):
        client = FakeClient(calc_then_answer())
        final, trace = load("agent.py").run_with_trace(client, "x")
        call = trace[0]
        assert call["type"] == "tool_call"
        assert call["name"] == "calculate"
        assert call["input"] == {"expression": "17 * 23"}
        assert call["result"] == "391"
        assert trace[1]["type"] == "answer"

    def test_steps_are_numbered_from_one(self, load):
        client = FakeClient(calc_then_answer())
        _, trace = load("agent.py").run_with_trace(client, "x")
        assert [entry["step"] for entry in trace] == [1, 2]


class TestShow:
    TRACE = [
        {"step": 1, "type": "tool_call", "name": "calculate",
         "input": {"expression": "17 * 23"}, "result": "391"},
        {"step": 2, "type": "answer", "text": "17 * 23 is 391."},
    ]

    def test_format_a_tool_call(self, load):
        assert load("show.py").format_step(self.TRACE[0]) == (
            "1. calculate({'expression': '17 * 23'}) -> 391"
        )

    def test_format_an_answer(self, load):
        assert load("show.py").format_step(self.TRACE[1]) == (
            "2. answer: 17 * 23 is 391."
        )

    def test_format_trace(self, load):
        assert load("show.py").format_trace(self.TRACE) == (
            "1. calculate({'expression': '17 * 23'}) -> 391\n"
            "2. answer: 17 * 23 is 391."
        )

    def test_format_empty_trace(self, load):
        assert load("show.py").format_trace([]) == ""

    def test_tool_names_keeps_repeats_and_order(self, load):
        trace = [
            {"step": 1, "type": "tool_call", "name": "calculate", "input": {}, "result": ""},
            {"step": 2, "type": "tool_call", "name": "city_info", "input": {}, "result": ""},
            {"step": 3, "type": "tool_call", "name": "calculate", "input": {}, "result": ""},
            {"step": 4, "type": "answer", "text": "done"},
        ]
        assert load("show.py").tool_names(trace) == [
            "calculate", "city_info", "calculate",
        ]

    def test_summarise(self, load):
        trace = [
            {"step": 1, "type": "tool_call", "name": "calculate", "input": {}, "result": ""},
            {"step": 2, "type": "tool_call", "name": "city_info", "input": {}, "result": ""},
            {"step": 3, "type": "answer", "text": "done"},
        ]
        assert load("show.py").summarise(trace) == (
            "3 steps, 2 tool calls (calculate, city_info)"
        )

    def test_summarise_with_no_tools(self, load):
        trace = [{"step": 1, "type": "answer", "text": "done"}]
        assert load("show.py").summarise(trace) == "1 steps, 0 tool calls ()"


class TestNoFrameworks:
    @pytest.mark.parametrize("name", ["agent.py", "show.py"])
    def test_the_fence(self, load, source, name):
        load(name)
        code = source(name, code_only=True)
        assert code.strip(), (
            f"{name} has nothing in it yet - write it first."
        )
        code = code.lower()
        for banned in ("langchain", "langgraph", "crewai", "autogen", "smolagents"):
            assert banned not in code, (
                f"{name} imports {banned}. Not this week - and next week you have "
                "to write down what the framework bought you, which you cannot do "
                "if you never built the thing it replaces."
            )

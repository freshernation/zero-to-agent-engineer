"""Week 6, Day 1 - the Messages API.

Run me:  pytest week-06/day-1 -v

Every test hands your function a FakeClient. No key, no network, no cost, and the
same answer every run.
"""

import pytest
from fake_model import (
    FakeClient, Message, TextBlock, ToolUseBlock, Usage, text_reply,
)


class TestAsk:
    def test_returns_the_reply_text(self, load):
        client = FakeClient([text_reply("A token is a chunk of text.")])
        assert load("call.py").ask(client, "What is a token?") == (
            "A token is a chunk of text."
        )

    def test_sends_the_question_as_a_user_message(self, load):
        client = FakeClient([text_reply("ok")])
        load("call.py").ask(client, "What is a token?")
        sent = client.last_call["messages"]
        assert sent == [{"role": "user", "content": "What is a token?"}], (
            f"Sent {sent}. messages is a list of dicts with role and content, "
            "and it has to start with a user turn."
        )

    def test_passes_max_tokens(self, load):
        client = FakeClient([text_reply("ok")])
        load("call.py").ask(client, "hi", max_tokens=50)
        assert client.last_call["max_tokens"] == 50, (
            "max_tokens is required by the API - pass it through."
        )

    def test_passes_the_model(self, load):
        client = FakeClient([text_reply("ok")])
        load("call.py").ask(client, "hi", model="claude-opus-4-5")
        assert client.last_call["model"] == "claude-opus-4-5"

    def test_calls_the_model_once(self, load):
        client = FakeClient([text_reply("ok")])
        load("call.py").ask(client, "hi")
        assert client.call_count == 1


class TestExtractText:
    def test_single_block(self, load):
        response = Message([TextBlock("hello")])
        assert load("call.py").extract_text(response) == "hello"

    def test_joins_several_blocks(self, load):
        response = Message([TextBlock("one "), TextBlock("two")])
        assert load("call.py").extract_text(response) == "one two"

    def test_ignores_non_text_blocks(self, load):
        """From next week a response can contain tool calls too."""
        response = Message([
            TextBlock("Let me check. "),
            ToolUseBlock("get_weather", {"city": "Lisbon"}),
        ])
        assert load("call.py").extract_text(response) == "Let me check. ", (
            "Skip blocks whose .type is not 'text'. content[0].text works until "
            "the day the first block is a tool call."
        )

    def test_no_text_blocks_at_all(self, load):
        response = Message([ToolUseBlock("x", {})])
        assert load("call.py").extract_text(response) == ""


class TestTruncation:
    def test_detects_truncation(self, load):
        cut = Message([TextBlock("It was the best of")], stop_reason="max_tokens")
        assert load("call.py").was_truncated(cut) is True

    def test_normal_finish(self, load):
        assert load("call.py").was_truncated(text_reply("done")) is False

    def test_ask_safely_returns_the_reply(self, load):
        client = FakeClient([text_reply("a complete answer")])
        assert load("call.py").ask_safely(client, "hi") == "a complete answer"

    def test_ask_safely_returns_none_when_cut_off(self, load):
        cut = Message([TextBlock("It was the best of")], stop_reason="max_tokens")
        client = FakeClient([cut])
        assert load("call.py").ask_safely(client, "hi", max_tokens=5) is None, (
            "A truncated reply is a complete-looking sentence that is missing "
            "the end. Check stop_reason before you use a response."
        )


class TestConversation:
    def test_build_messages_alternates(self, load):
        built = load("conversation.py").build_messages(["hi", "hello", "how are you"])
        assert built == [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
            {"role": "user", "content": "how are you"},
        ]

    def test_build_messages_of_nothing(self, load):
        assert load("conversation.py").build_messages([]) == []

    def test_add_turn_returns_a_new_list(self, load):
        original = [{"role": "user", "content": "hi"}]
        result = load("conversation.py").add_turn(original, "assistant", "hello")
        assert len(result) == 2
        assert len(original) == 1, (
            "add_turn changed the list it was given. Same rule as week 3's "
            "add_expense - take values in, hand new ones back."
        )

    @pytest.mark.parametrize("messages,valid", [
        ([], True),
        ([{"role": "user", "content": "a"}], True),
        ([{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}], True),
        ([{"role": "assistant", "content": "b"}], False),
        ([{"role": "user", "content": "a"}, {"role": "user", "content": "b"}], False),
    ])
    def test_is_valid(self, load, messages, valid):
        assert load("conversation.py").is_valid(messages) is valid

    def test_continue_chat_sends_the_whole_history(self, load):
        client = FakeClient([text_reply("I am well")])
        history = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
        reply = load("conversation.py").continue_chat(client, history, "how are you")
        assert reply == "I am well"
        sent = client.last_call["messages"]
        assert len(sent) == 3, (
            f"Sent {len(sent)} messages. The model has no memory - a conversation "
            "is you resending the entire history every single call."
        )
        assert sent[-1] == {"role": "user", "content": "how are you"}


class TestAccounting:
    def test_token_cost(self, load):
        usage = Usage(input_tokens=1000, output_tokens=500)
        assert load("accounting.py").token_cost(usage, 3.0, 15.0) == 0.0105

    def test_token_cost_rounds_to_six_places(self, load):
        usage = Usage(input_tokens=120, output_tokens=45)
        assert load("accounting.py").token_cost(usage, 3.0, 15.0) == 0.001035

    def test_total_tokens(self, load):
        assert load("accounting.py").total_tokens(Usage(120, 45)) == 165

    @pytest.mark.parametrize("text,tokens", [
        ("", 0), ("abcd", 1), ("abcde", 2), ("a" * 400, 100), ("a" * 401, 101),
    ])
    def test_estimate_tokens_rounds_up(self, load, text, tokens):
        assert load("accounting.py").estimate_tokens(text) == tokens

    def test_describe(self, load):
        response = Message([TextBlock("x")], usage=Usage(120, 45))
        assert load("accounting.py").describe(response, 3.0, 15.0) == (
            "120 in, 45 out, $0.001035"
        )

    def test_rates_are_not_hard_coded(self, load, source):
        load("accounting.py").token_cost
        code = source("accounting.py", code_only=True)
        body = code.split("def token_cost")[-1].split("def ")[0]
        assert "15.0" not in body and "15." not in body.replace("15.0", ""), (
            "A price is baked into token_cost. Rates change - take them as "
            "arguments, which is what the signature already asks for."
        )

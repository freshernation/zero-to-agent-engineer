"""Week 6, Day 4 - memory, streaming and failure.

Run me:  pytest week-06/day-4 -v
"""

import pytest
from fake_model import FakeClient, ModelError, Usage, text_reply

PLACEHOLDER = "(your answer)"

FIVE = [
    {"role": "user", "content": "one"},
    {"role": "assistant", "content": "two"},
    {"role": "user", "content": "three"},
    {"role": "assistant", "content": "four"},
    {"role": "user", "content": "five"},
]


class TestTrim:
    def test_short_history_is_untouched(self, load):
        assert load("memory.py").trim(FIVE, 10) == FIVE

    def test_keeps_the_most_recent(self, load):
        trimmed = load("memory.py").trim(FIVE, 3)
        assert trimmed[-1]["content"] == "five"

    @pytest.mark.parametrize("max_turns", [1, 2, 3, 4, 5])
    def test_always_starts_with_user(self, load, max_turns):
        trimmed = load("memory.py").trim(FIVE, max_turns)
        if trimmed:
            assert trimmed[0]["role"] == "user", (
                f"trim(messages, {max_turns}) left the history starting with an "
                "assistant turn. A real API rejects that outright - drop in "
                "pairs, not one at a time."
            )

    def test_empty(self, load):
        assert load("memory.py").trim([], 3) == []


class TestEstimates:
    def test_estimate_rounds_up_per_message(self, load):
        messages = [{"role": "user", "content": "abcde"}]
        assert load("memory.py").estimate_conversation_tokens(messages) == 2

    def test_estimate_adds_up(self, load):
        messages = [
            {"role": "user", "content": "a" * 400},
            {"role": "assistant", "content": "b" * 400},
        ]
        assert load("memory.py").estimate_conversation_tokens(messages) == 200

    def test_needs_trimming(self, load):
        mod = load("memory.py")
        big = [{"role": "user", "content": "a" * 4000}]
        assert mod.needs_trimming(big, 100) is True
        assert mod.needs_trimming(big, 10_000) is False


class TestConversation:
    def test_starts_empty(self, load):
        chat = load("memory.py").Conversation()
        assert len(chat) == 0
        assert chat.messages == []

    def test_records_turns(self, load):
        chat = load("memory.py").Conversation()
        chat.add_user("hi")
        chat.add_assistant("hello")
        assert len(chat) == 2
        assert chat.messages[0] == {"role": "user", "content": "hi"}

    def test_send_records_both_sides(self, load):
        chat = load("memory.py").Conversation()
        client = FakeClient([text_reply("hello there")])
        assert chat.send(client, "hi") == "hello there"
        assert len(chat) == 2
        assert chat.messages[-1] == {"role": "assistant", "content": "hello there"}

    def test_send_includes_the_history(self, load):
        chat = load("memory.py").Conversation()
        client = FakeClient([text_reply("a"), text_reply("b")])
        chat.send(client, "first")
        chat.send(client, "second")
        assert len(client.calls[1]["messages"]) == 3, (
            "The second call should carry both earlier turns plus the new "
            "question. The model remembers nothing."
        )

    def test_send_passes_the_system_prompt(self, load):
        chat = load("memory.py").Conversation(system="Be terse.")
        client = FakeClient([text_reply("ok")])
        chat.send(client, "hi")
        assert client.last_call.get("system") == "Be terse."

    def test_messages_are_trimmed(self, load):
        chat = load("memory.py").Conversation(max_turns=2)
        client = FakeClient(text_reply("ok"))
        for _ in range(4):
            chat.send(client, "hi")
        assert len(chat.messages) <= 2
        assert chat.messages[0]["role"] == "user"

    def test_total_cost(self, load):
        chat = load("memory.py").Conversation()
        client = FakeClient([text_reply("a", input_tokens=1000, output_tokens=500)])
        chat.send(client, "hi")
        assert chat.total_cost(3.0, 15.0) == 0.0105

    def test_total_cost_accumulates(self, load):
        chat = load("memory.py").Conversation()
        client = FakeClient(text_reply("a", input_tokens=1000, output_tokens=500))
        chat.send(client, "hi")
        chat.send(client, "hi again")
        assert chat.total_cost(3.0, 15.0) == 0.021


class TestStreaming:
    def test_stream_reply_assembles_the_chunks(self, load):
        client = FakeClient([text_reply("streaming works fine")])
        assert load("streaming.py").stream_reply(client, "hi") == (
            "streaming works fine"
        )

    def test_stream_to_calls_write_for_each_chunk(self, load):
        client = FakeClient([text_reply("streaming works fine")])
        chunks = []
        result = load("streaming.py").stream_to(client, "hi", chunks.append)
        assert result == "streaming works fine"
        assert len(chunks) > 1, (
            "write() was called once, so nothing was actually streamed - you "
            "waited for the whole reply and then handed it over."
        )
        assert "".join(chunks) == "streaming works fine"

    def test_stream_with_usage(self, load):
        client = FakeClient([text_reply("hello", input_tokens=7, output_tokens=3)])
        text, usage = load("streaming.py").stream_with_usage(client, "hi")
        assert text == "hello"
        assert usage.input_tokens == 7 and usage.output_tokens == 3


class TestResilient:
    def test_succeeds_first_time(self, load):
        client = FakeClient([text_reply("fine")])
        assert load("resilient.py").call_with_retry(client, "hi") == "fine"

    def test_recovers_after_a_failure(self, load):
        client = FakeClient([ModelError("overloaded"), text_reply("fine")])
        assert load("resilient.py").call_with_retry(client, "hi") == "fine"

    def test_gives_up(self, load):
        client = FakeClient([ModelError("x")] * 3)
        assert load("resilient.py").call_with_retry(client, "hi", attempts=3) is None

    def test_attempts_used(self, load):
        client = FakeClient([ModelError("x"), ModelError("x"), text_reply("fine")])
        assert load("resilient.py").attempts_used(client, "hi") == 3

    def test_stops_as_soon_as_it_works(self, load):
        client = FakeClient([text_reply("fine")])
        load("resilient.py").call_with_retry(client, "hi")
        assert client.call_count == 1, (
            "It kept calling after a success. Stop at the first working answer."
        )

    def test_safe_call_returns_the_reply(self, load):
        client = FakeClient([text_reply("fine")])
        assert load("resilient.py").safe_call(client, "hi") == "fine"

    def test_safe_call_never_raises(self, load):
        client = FakeClient([ModelError("x")] * 10)
        assert load("resilient.py").safe_call(client, "hi") == (
            "Sorry, I could not answer that."
        )

    def test_safe_call_custom_fallback(self, load):
        client = FakeClient([ModelError("x")] * 10)
        assert load("resilient.py").safe_call(client, "hi", fallback="nope") == "nope"


class TestFixes:
    def test_broken_1_trims_in_pairs(self, run):
        r = run("broken_1.py")
        r.expect("Turns: 3")
        r.expect("Starts with: user")

    def test_broken_2_uses_the_output_rate(self, run):
        run("broken_2.py").expect("Cost: $0.000225")

    def test_broken_3_stops_and_narrows(self, run, source):
        run("broken_3.py").expect("Reply: All good")
        code = source("broken_3.py", code_only=True)
        assert "except Exception" not in code and "except:" not in code, (
            "The broad except is still there. It hid the reason the first "
            "attempt failed, and it would hide your own mistakes too."
        )
        assert "break" in code, (
            "Nothing stops the loop after a successful call, so a later attempt "
            "overwrites a good answer with a worse one."
        )


class TestNotes:
    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_entry_is_filled_in(self, source, n):
        text = source("NOTES.md")
        parts = text.split(f"## broken_{n}.py")
        assert len(parts) > 1, f"NOTES.md is missing the broken_{n}.py section."
        body = parts[1].split("\n## ")[0]
        assert PLACEHOLDER not in body, (
            f"The broken_{n}.py entry still has '{PLACEHOLDER}' placeholders."
        )
        assert len(body.split()) >= 40, (
            f"The broken_{n}.py entry is too short. Answer all four prompts."
        )

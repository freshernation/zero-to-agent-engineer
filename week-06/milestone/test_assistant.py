"""Week 6 milestone - the assistant.

Run me:  pytest week-06/milestone -v

All of this runs against FakeClient. No key, no network, no cost.
"""

import pytest
from fake_model import FakeClient, ModelError, text_reply
from pydantic import ValidationError

NOTE_JSON = (
    '{"title": "Buy milk", "body": "Buy milk on the way home", '
    '"tags": ["shopping", "urgent"], "priority": 1}'
)
BARE_NOTE_JSON = '{"title": "Read book", "body": "Finish chapter 3"}'


class TestConversation:
    def test_starts_empty(self, load):
        chat = load("chat.py").Conversation()
        assert chat.turn_count == 0
        assert chat.messages == []
        assert chat.total_cost(3.0, 15.0) == 0

    def test_send_records_both_sides(self, load):
        chat = load("chat.py").Conversation()
        client = FakeClient([text_reply("hello there")])
        assert chat.send(client, "hi") == "hello there"
        assert chat.turn_count == 2
        assert chat.messages[-1] == {"role": "assistant", "content": "hello there"}

    def test_send_carries_the_history(self, load):
        chat = load("chat.py").Conversation()
        client = FakeClient(text_reply("ok"))
        chat.send(client, "first")
        chat.send(client, "second")
        assert len(client.calls[1]["messages"]) == 3

    def test_system_prompt_is_sent(self, load):
        chat = load("chat.py").Conversation(system="Be terse.")
        client = FakeClient([text_reply("ok")])
        chat.send(client, "hi")
        assert client.last_call.get("system") == "Be terse."

    def test_trimming_keeps_it_valid(self, load):
        chat = load("chat.py").Conversation(max_turns=4)
        client = FakeClient(text_reply("ok"))
        for _ in range(6):
            chat.send(client, "hi")
        assert len(chat.messages) <= 4
        assert chat.messages[0]["role"] == "user"

    def test_stream_returns_and_records(self, load):
        chat = load("chat.py").Conversation()
        client = FakeClient([text_reply("streamed answer")])
        chunks = []
        assert chat.stream(client, "hi", chunks.append) == "streamed answer"
        assert "".join(chunks) == "streamed answer"
        assert len(chunks) > 1, "Nothing was actually streamed."
        assert chat.turn_count == 2, (
            "A streamed turn is still a turn - record the reply in the history."
        )

    def test_cost_accumulates(self, load):
        chat = load("chat.py").Conversation()
        client = FakeClient(text_reply("a", input_tokens=1000, output_tokens=500))
        chat.send(client, "hi")
        chat.send(client, "again")
        assert chat.total_cost(3.0, 15.0) == 0.021

    def test_reset_clears_everything(self, load):
        chat = load("chat.py").Conversation()
        client = FakeClient(text_reply("a", input_tokens=1000, output_tokens=500))
        chat.send(client, "hi")
        chat.reset()
        assert chat.turn_count == 0
        assert chat.messages == []
        assert chat.total_cost(3.0, 15.0) == 0, (
            "reset() forgets the cost too - it is a fresh session."
        )


class TestNote:
    def test_defaults(self, load):
        note = load("extract.py").Note(title="t", body="b")
        assert note.tags == []
        assert note.priority == 2

    @pytest.mark.parametrize("kwargs", [
        {"title": "", "body": "b"},
        {"title": "t", "body": ""},
        {"title": "t", "body": "b", "priority": 0},
        {"title": "t", "body": "b", "priority": 4},
    ])
    def test_rejects(self, load, kwargs):
        Note = load("extract.py").Note
        with pytest.raises(ValidationError):
            Note(**kwargs)

    def test_tags_are_independent_between_notes(self, load):
        Note = load("extract.py").Note
        first = Note(title="a", body="b")
        first.tags.append("x")
        assert Note(title="c", body="d").tags == [], (
            "The two notes share one tags list. pydantic handles this correctly "
            "on its own - if you see this fail, something unusual is going on."
        )


class TestExtractNote:
    def test_system_names_every_field(self, load):
        system = load("extract.py").build_note_system()
        for field in ("title", "body", "tags", "priority"):
            assert field in system

    def test_clean_reply(self, load):
        client = FakeClient([text_reply(NOTE_JSON)])
        note = load("extract.py").extract_note(client, "buy milk")
        assert note.title == "Buy milk"
        assert note.tags == ["shopping", "urgent"]
        assert note.priority == 1

    def test_wrapped_reply(self, load):
        client = FakeClient([text_reply(f"Sure!\n```json\n{NOTE_JSON}\n```")])
        assert load("extract.py").extract_note(client, "x").title == "Buy milk"

    def test_defaults_fill_in(self, load):
        client = FakeClient([text_reply(BARE_NOTE_JSON)])
        note = load("extract.py").extract_note(client, "x")
        assert note.tags == [] and note.priority == 2

    def test_retries_once(self, load):
        client = FakeClient([text_reply("no json here"), text_reply(NOTE_JSON)])
        assert load("extract.py").extract_note(client, "x").title == "Buy milk"

    def test_gives_up(self, load):
        client = FakeClient([text_reply("nope")] * 2)
        assert load("extract.py").extract_note(client, "x", attempts=2) is None

    def test_uses_temperature_zero(self, load):
        client = FakeClient([text_reply(NOTE_JSON)])
        load("extract.py").extract_note(client, "x")
        assert client.last_call.get("temperature") == 0


class TestAssistantCli:
    def test_streams_a_reply(self, run):
        run("assistant.py", answers=["hello", "/quit"]).expect("This is a fake reply.")

    def test_cost_command(self, run):
        r = run("assistant.py", answers=["hi", "/cost", "/quit"])
        assert "Spent so far: $" in r.stdout

    def test_turns_command(self, run):
        r = run("assistant.py", answers=["hi", "hi again", "/turns", "/quit"])
        r.expect("Turns: 4")

    def test_reset_command(self, run):
        r = run("assistant.py", answers=["hi", "/reset", "/turns", "/quit"])
        r.expect("Forgotten.")
        r.expect("Turns: 0")

    def test_unknown_command(self, run):
        run("assistant.py", answers=["/banana", "/quit"]).expect(
            "Unknown command: /banana"
        )

    def test_a_plain_message_is_not_a_command(self, run):
        r = run("assistant.py", answers=["cost", "/quit"])
        r.expect("Total: $")  # nothing to check until the loop runs at all
        assert "Unknown command" not in r.stdout, (
            "'cost' with no slash is a message, not a command."
        )

    def test_quit_prints_the_total(self, run):
        r = run("assistant.py", answers=["/quit"])
        r.expect("Total: $0.000000")

    def test_note_command(self, run):
        """The fake client answers a JSON system prompt with JSON, so a correct
        build_note_system() makes this work end to end."""
        r = run("assistant.py", answers=["/note buy milk", "/quit"])
        assert "Note:" in r.stdout, (
            "/note printed no note.\n"
            "The fake client returns a JSON object when the system prompt asks "
            "for one and lists the keys after 'keys:'. If your prompt says that, "
            "this works; if it does not, the model has to guess the shape - and a "
            "real one guesses wrong too.\n\n"
            f"What it printed:\n{r.stdout}"
        )

    def test_note_failure_is_handled(self, run):
        """Nothing a person types may produce a traceback."""
        r = run("assistant.py", answers=["/note ", "/quit"])
        r.expect("Could not extract a note.")
        assert "Traceback" not in r.stderr, (
            "A note that cannot be extracted must not produce a traceback."
        )


class TestLayering:
    @pytest.mark.parametrize("name,attribute", [
        ("chat.py", "Conversation"), ("extract.py", "Note"),
    ])
    def test_no_printing_or_input(self, load, source, name, attribute):
        getattr(load(name), attribute)
        code = source(name, code_only=True)
        assert "print(" not in code, f"{name} contains a print()."
        assert "input(" not in code, f"{name} contains an input()."

    def test_no_key_in_the_source(self, load, source):
        load("chat.py").Conversation
        for name in ("chat.py", "extract.py", "assistant.py"):
            code = source(name, code_only=True)
            assert "sk-ant" not in code, f"There is a key in {name}."

    def test_every_call_caps_max_tokens(self, load, source):
        load("chat.py").Conversation
        for name in ("chat.py", "extract.py"):
            assert "max_tokens" in source(name, code_only=True), (
                f"{name} makes a model call without max_tokens, which the API "
                "requires."
            )

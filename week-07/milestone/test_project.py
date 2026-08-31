"""Project 2 - the agent.

Run me:  pytest week-07/milestone -v

All against FakeClient. No key, no network, no cost.
"""

import re
from pathlib import Path

import pytest
from fake_model import FakeClient, Message, ToolUseBlock, text_reply, tool_reply

REQUIRED_TOOLS = {"calculate", "save_note", "list_notes", "read_note"}


@pytest.fixture(autouse=True)
def clean_notes(request):
    notes = Path(request.fspath).parent / "notes.json"
    notes.unlink(missing_ok=True)
    yield
    notes.unlink(missing_ok=True)


class TestTools:
    @pytest.mark.parametrize("expression,answer", [
        ("2+2", 4), ("17 * 23", 391), ("(2 + 3) * 4", 20),
    ])
    def test_calculate(self, load, expression, answer):
        assert load("tools.py").calculate(expression) == answer

    @pytest.mark.parametrize("expression", [
        "__import__('os').system('ls')", "open('/etc/passwd')", "print(1)",
    ])
    def test_calculate_refuses_code(self, load, expression):
        with pytest.raises(ValueError) as caught:
            load("tools.py").calculate(expression)
        assert "Unsafe expression" in str(caught.value)

    def test_notes_start_empty(self, load):
        assert load("tools.py").list_notes() == "No notes yet."

    def test_save_and_read(self, load):
        mod = load("tools.py")
        assert mod.save_note("Shopping", "milk and bread") == "Saved note: Shopping"
        assert mod.read_note("Shopping") == "milk and bread"

    def test_list_notes(self, load):
        mod = load("tools.py")
        mod.save_note("Shopping", "milk")
        mod.save_note("Ideas", "a good one")
        listed = mod.list_notes()
        assert "Shopping" in listed and "Ideas" in listed

    def test_read_a_note_that_is_not_there(self, load):
        assert load("tools.py").read_note("Nothing") == "No note called Nothing."

    def test_notes_survive_a_reload(self, load):
        """State the agent can rely on between tool calls."""
        load("tools.py").save_note("Shopping", "milk")
        assert load("tools.py").read_note("Shopping") == "milk"

    def test_tools_know_nothing_about_models(self, load, source):
        load("tools.py").calculate
        code = source("tools.py", code_only=True).lower()
        for banned in ("anthropic", "fake_model", "messages.create"):
            assert banned not in code, (
                f"tools.py mentions {banned}. Tools are ordinary functions - "
                "that is the whole point of the separation."
            )


class TestSchemas:
    def test_covers_every_required_tool(self, load):
        names = {s["name"] for s in load("schemas.py").all_schemas()}
        assert REQUIRED_TOOLS <= names, f"Missing schemas for {REQUIRED_TOOLS - names}"

    def test_has_a_tool_of_your_own(self, load):
        names = {s["name"] for s in load("schemas.py").all_schemas()}
        extra = names - REQUIRED_TOOLS
        assert extra, (
            "Add at least one tool of your own. Something real and offline."
        )

    def test_descriptions_are_written(self, load):
        for schema in load("schemas.py").all_schemas():
            words = len(schema["description"].split())
            assert words >= 8, (
                f"{schema['name']}'s description is {words} words. That "
                "description is the only thing the model knows about your "
                "function - say what it does and when to use it."
            )

    def test_every_schema_is_well_formed(self, load):
        for schema in load("schemas.py").all_schemas():
            assert schema["input_schema"]["type"] == "object"
            assert isinstance(schema["input_schema"]["properties"], dict)
            assert isinstance(schema["input_schema"]["required"], list)


class TestAgent:
    def test_plain_answer(self, load):
        agent = load("agent.py").Agent(FakeClient([text_reply("Paris.")]))
        assert agent.run("Capital?") == "Paris."
        assert agent.stop_reason == "answered"
        assert agent.model_calls == 1

    def test_one_tool(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "17 * 23"}, id="t1"),
            text_reply("It is 391."),
        ])
        agent = load("agent.py").Agent(client)
        assert agent.run("17 * 23?") == "It is 391."
        assert agent.trace[0]["result"] == "391"

    def test_two_tools_in_sequence_with_state(self, load):
        """The run that proves it is an agent: the second tool uses the first's answer."""
        client = FakeClient([
            tool_reply("calculate", {"expression": "17 * 23"}, id="t1"),
            tool_reply("save_note", {"title": "Maths", "body": "391"}, id="t2"),
            text_reply("Saved note: Maths"),
        ])
        agent = load("agent.py").Agent(client)
        assert agent.run("work it out and save it") == "Saved note: Maths"
        assert load("tools.py").read_note("Maths") == "391"

    def test_several_tools_in_one_response(self, load):
        client = FakeClient([
            Message(
                [
                    ToolUseBlock("calculate", {"expression": "2+2"}, "t1"),
                    ToolUseBlock("list_notes", {}, "t2"),
                ],
                stop_reason="tool_use",
            ),
            text_reply("Both done."),
        ])
        agent = load("agent.py").Agent(client)
        assert agent.run("two at once") == "Both done."
        assert len([e for e in agent.trace if e["type"] == "tool_call"]) == 2

    def test_last_answer(self, load):
        agent = load("agent.py").Agent(FakeClient([text_reply("Paris.")]))
        agent.run("x")
        assert agent.last_answer == "Paris."


class TestAgentSurvives:
    def test_unknown_tool(self, load):
        client = FakeClient([
            tool_reply("search_web", {"q": "x"}, id="t1"),
            text_reply("I do not have that tool."),
        ])
        agent = load("agent.py").Agent(client)
        agent.run("look it up")
        assert agent.stop_reason == "answered"
        assert "Unknown tool: search_web" in agent.trace[0]["result"]

    def test_tool_that_raises(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": "rm -rf /"}, id="t1"),
            text_reply("I could not do that."),
        ])
        agent = load("agent.py").Agent(client)
        agent.run("x")
        assert agent.stop_reason == "answered"
        assert "Tool failed" in agent.trace[0]["result"]

    def test_missing_argument(self, load):
        client = FakeClient([
            tool_reply("calculate", {}, id="t1"),
            text_reply("Trying again."),
        ])
        agent = load("agent.py").Agent(client)
        agent.run("x")
        assert agent.stop_reason == "answered"
        assert "Tool failed" in agent.trace[0]["result"]

    def test_results_are_truncated(self, load):
        client = FakeClient([
            tool_reply("save_note", {"title": "Big", "body": "x" * 2000}, id="t1"),
            tool_reply("read_note", {"title": "Big"}, id="t2"),
            text_reply("done"),
        ])
        agent = load("agent.py").Agent(client)
        agent.run("x")
        for entry in agent.trace:
            if entry["type"] == "tool_call":
                assert len(entry["result"]) <= 520

    def test_repeat_detection(self, load):
        client = FakeClient(tool_reply("calculate", {"expression": "2+2"}, id="t1"))
        agent = load("agent.py").Agent(client, max_iterations=10, max_repeats=2)
        assert agent.run("circles") == (
            "Stopped: the agent repeated the same tool call."
        )
        assert agent.stop_reason == "looping"
        assert agent.model_calls < 10

    def test_the_cap(self, load):
        client = FakeClient([
            tool_reply("calculate", {"expression": f"{n}+{n}"}, id=f"t{n}")
            for n in range(20)
        ])
        agent = load("agent.py").Agent(client, max_iterations=4, max_repeats=3)
        assert agent.run("keep going") == "Stopped after 4 steps without finishing."
        assert agent.stop_reason == "cap"


class TestCli:
    def test_answers(self, run):
        run("cli.py", answers=["hello", "/quit"]).expect("Bye.")

    def test_trace_before_any_run(self, run):
        run("cli.py", answers=["/trace", "/quit"]).expect("No runs yet.")

    def test_trace_after_a_run(self, run):
        r = run("cli.py", answers=["hello", "/trace", "/quit"])
        assert "answer:" in r.stdout, (
            "/trace should show the last run, one line per step."
        )

    def test_stop_command(self, run):
        r = run("cli.py", answers=["hello", "/stop", "/quit"])
        r.expect("Stop reason: answered")

    def test_no_traceback_on_anything(self, run):
        r = run("cli.py", answers=["", "/nonsense", "hello", "/quit"])
        r.expect("Bye.")  # it has to get to the end at all
        assert "Traceback" not in r.stderr


class TestNoFrameworks:
    @pytest.mark.parametrize("name", ["tools.py", "schemas.py", "agent.py", "cli.py"])
    def test_the_fence(self, load, source, name):
        load(name)
        code = source(name, code_only=True)
        assert code.strip(), (
            f"{name} has nothing in it yet - write it first."
        )
        code = code.lower()
        for banned in ("langchain", "langgraph", "crewai", "autogen", "llama_index"):
            assert banned not in code, (
                f"{name} imports {banned}. Next week you have to write down what "
                "the framework bought you - which needs this version to exist first."
            )


class TestWriteup:
    HEADINGS = [
        "The loop",
        "What a tool is",
        "Why there is a cap",
        "What went wrong",
        "What a framework would do",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_exists_and_is_written(self, source, heading):
        text = source("WRITEUP.md")
        assert f"## {heading}" in text, f"WRITEUP.md has no '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, (
            f"The '{heading}' section is {len(body.split())} words. This "
            "document is the thing that gets you asked good questions in an "
            "interview - it is worth an hour."
        )

    def test_long_enough(self, source):
        text = source("WRITEUP.md")
        body = text.split("-->")[-1]
        for heading in self.HEADINGS:
            body = body.replace(f"## {heading}", "")
        assert len(body.split()) >= 500, (
            f"WRITEUP.md is {len(body.split())} words of content, and needs 500."
        )

    @pytest.mark.parametrize("idea", ["stop_reason", "tool_use_id", "cap"])
    def test_mentions_the_load_bearing_ideas(self, source, idea):
        # strip the instructions comment and the headings themselves - both
        # contain the words being looked for, so an untouched stub would pass
        raw = source("WRITEUP.md")
        body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
        for heading in self.HEADINGS:
            body = body.replace(f"## {heading}", "")
        text = body.lower()
        assert idea.lower() in text, (
            f"WRITEUP.md never mentions '{idea}'. A write-up that misses it was "
            "not written from understanding - go back to the code and work out "
            "what it does before describing it."
        )

    def test_written_by_you(self, source):
        text = source("WRITEUP.md")
        assert "<!--" not in text or "Write this AFTER" not in text, (
            "The instructions comment is still in WRITEUP.md. Delete it."
        )

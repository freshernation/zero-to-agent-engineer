"""Week 7, Day 1 - tool schemas and dispatch.

Run me:  pytest week-07/day-1 -v
"""

import pytest
from fake_model import Message, TextBlock, ToolUseBlock, tool_reply


class TestCalculate:
    @pytest.mark.parametrize("expression,answer", [
        ("2+2", 4), ("17 * 23", 391), ("10 / 4", 2.5),
        ("(2 + 3) * 4", 20), ("7 - 9", -2),
    ])
    def test_arithmetic(self, load, expression, answer):
        assert load("tools.py").calculate(expression) == answer

    @pytest.mark.parametrize("expression", [
        "__import__('os').system('ls')",
        "open('/etc/passwd').read()",
        "2 + abc",
        "print(1)",
    ])
    def test_refuses_anything_that_is_not_arithmetic(self, load, expression):
        with pytest.raises(ValueError) as caught:
            load("tools.py").calculate(expression)
        assert "Unsafe expression" in str(caught.value), (
            "Check the characters before evaluating. A tool that evaluates "
            "whatever it is handed is not a tool, it is a way in."
        )


class TestOtherTools:
    @pytest.mark.parametrize("text,count", [
        ("one two three", 3), ("hello", 1), ("", 0), ("  spaced   out  ", 2),
    ])
    def test_word_count(self, load, text, count):
        assert load("tools.py").word_count(text) == count

    def test_city_info(self, load):
        assert load("tools.py").city_info("Lisbon") == (
            "Lisbon is in Portugal, population 545000."
        )

    def test_unknown_city(self, load):
        assert load("tools.py").city_info("Narnia") == "I don't know about Narnia."


class TestSchemas:
    def test_text_param(self, load):
        assert load("schemas.py").text_param("the thing") == {
            "type": "string",
            "description": "the thing",
        }

    def test_make_schema_shape(self, load):
        mod = load("schemas.py")
        schema = mod.make_schema(
            "calculate", "Evaluate arithmetic.",
            {"expression": mod.text_param("the sum")}, ["expression"],
        )
        assert schema["name"] == "calculate"
        assert schema["description"] == "Evaluate arithmetic."
        assert schema["input_schema"]["type"] == "object"
        assert "expression" in schema["input_schema"]["properties"]
        assert schema["input_schema"]["required"] == ["expression"]

    def test_all_schemas_covers_every_tool(self, load):
        schemas = load("schemas.py").all_schemas()
        names = {schema["name"] for schema in schemas}
        assert names == {"calculate", "word_count", "city_info"}, (
            f"Got {names}. One schema per tool in tools.py."
        )

    def test_descriptions_are_written_not_placeholders(self, load):
        for schema in load("schemas.py").all_schemas():
            assert len(schema["description"].split()) >= 5, (
                f"The description for {schema['name']} is "
                f"{schema['description']!r}. That description IS the prompt - it "
                "is the only thing the model knows about your function. Say what "
                "it does and when to use it."
            )

    def test_every_schema_declares_its_arguments(self, load):
        for schema in load("schemas.py").all_schemas():
            properties = schema["input_schema"]["properties"]
            assert properties, f"{schema['name']} declares no arguments."
            assert schema["input_schema"]["required"], (
                f"{schema['name']} marks nothing as required."
            )


class TestDispatch:
    def test_table_has_every_tool(self, load):
        assert set(load("dispatch.py").TOOLS) == {
            "calculate", "word_count", "city_info",
        }

    def test_run_tool_returns_a_string(self, load):
        result = load("dispatch.py").run_tool("calculate", {"expression": "2+2"})
        assert result == "4", (
            f"Got {result!r}. A tool_result block carries a string - 4 and '4' "
            "are the same thing to the model."
        )

    def test_run_tool_with_several_arguments(self, load):
        assert load("dispatch.py").run_tool("word_count", {"text": "a b c"}) == "3"

    def test_run_tool_unknown_name(self, load):
        assert load("dispatch.py").run_tool("nonsense", {}) == "Unknown tool: nonsense", (
            "The model will occasionally invent a tool name. That is a normal "
            "thing to handle, not a crash."
        )

    def test_tool_uses_filters_out_text(self, load):
        response = Message(
            [TextBlock("Let me work that out."),
             ToolUseBlock("calculate", {"expression": "2+2"}, "t1")],
            stop_reason="tool_use",
        )
        uses = load("dispatch.py").tool_uses(response)
        assert len(uses) == 1
        assert uses[0].name == "calculate"

    def test_tool_uses_when_there_are_none(self, load):
        assert load("dispatch.py").tool_uses(Message([TextBlock("hi")])) == []

    def test_handle_response_pairs_ids_with_results(self, load):
        response = tool_reply("calculate", {"expression": "17 * 23"}, id="t9")
        assert load("dispatch.py").handle_response(response) == [("t9", "391")]

    def test_handle_response_with_several_calls(self, load):
        response = Message(
            [
                ToolUseBlock("calculate", {"expression": "2+2"}, "t1"),
                ToolUseBlock("word_count", {"text": "a b"}, "t2"),
            ],
            stop_reason="tool_use",
        )
        assert load("dispatch.py").handle_response(response) == [
            ("t1", "4"), ("t2", "2"),
        ]

    def test_handle_response_survives_a_tool_that_raises(self, load):
        response = tool_reply("calculate", {"expression": "rm -rf /"}, id="t1")
        results = load("dispatch.py").handle_response(response)
        assert len(results) == 1, "One call in, one result out - always."
        assert isinstance(results[0][1], str), (
            "A tool that raised still owes the model an answer. Catch it and "
            "return the message as the result - an agent that crashes because a "
            "tool failed cannot recover, and recovering is the whole point."
        )

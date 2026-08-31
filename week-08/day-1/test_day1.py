"""Week 8, Day 1 - LangChain's pieces.

Run me:  pytest week-08/day-1 -v
"""

import pytest
from fake_chat import FakeChat, ai, ai_tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

DICTS = [
    {"role": "system", "content": "Be terse."},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello"},
]


class TestMessages:
    def test_to_langchain(self, load):
        converted = load("messages.py").to_langchain(DICTS)
        assert isinstance(converted[0], SystemMessage)
        assert isinstance(converted[1], HumanMessage)
        assert isinstance(converted[2], AIMessage)
        assert converted[1].content == "Hi"

    def test_round_trip(self, load):
        mod = load("messages.py")
        assert mod.to_dicts(mod.to_langchain(DICTS)) == DICTS

    def test_describe(self, load):
        mod = load("messages.py")
        assert mod.describe(mod.to_langchain(DICTS)) == "system, human, ai"

    def test_describe_empty(self, load):
        assert load("messages.py").describe([]) == ""

    def test_last_ai_text(self, load):
        mod = load("messages.py")
        assert mod.last_ai_text(mod.to_langchain(DICTS)) == "Hello"

    def test_last_ai_text_when_there_is_none(self, load):
        assert load("messages.py").last_ai_text([HumanMessage("hi")]) is None


class TestTools:
    def test_all_four_exist(self, load):
        names = {t.name for t in load("tools.py").all_tools()}
        assert names == {"calculate", "word_count", "city_info", "reverse_text"}

    def test_calculate(self, load):
        calculate = load("tools.py").tool_by_name("calculate")
        assert calculate.invoke({"expression": "17 * 23"}) == "391"

    def test_calculate_refuses_code(self, load):
        calculate = load("tools.py").tool_by_name("calculate")
        with pytest.raises(ValueError):
            calculate.invoke({"expression": "__import__('os')"})

    def test_word_count(self, load):
        assert load("tools.py").tool_by_name("word_count").invoke(
            {"text": "one two three"}
        ) == "3"

    def test_city_info(self, load):
        city_info = load("tools.py").tool_by_name("city_info")
        assert city_info.invoke({"city": "Lisbon"}) == (
            "Lisbon is in Portugal, population 545000."
        )
        assert city_info.invoke({"city": "Narnia"}) == "I don't know about Narnia."

    def test_reverse_text(self, load):
        assert load("tools.py").tool_by_name("reverse_text").invoke(
            {"text": "abc"}
        ) == "cba"

    def test_tool_by_name_unknown(self, load):
        assert load("tools.py").tool_by_name("nonsense") is None

    def test_the_decorator_built_the_schema(self, load):
        """Everything you hand-wrote in week 7's schemas.py, generated."""
        calculate = load("tools.py").tool_by_name("calculate")
        assert "expression" in calculate.args, (
            "The @tool decorator reads the type hints. Annotate the argument."
        )
        assert calculate.args["expression"]["type"] == "string"

    def test_docstrings_are_real(self, load):
        for tool in load("tools.py").all_tools():
            words = len(tool.description.split())
            assert words >= 6, (
                f"{tool.name}'s description is {words} words. The decorator uses "
                "the docstring as the description, which means the docstring is "
                "now the prompt - it is the only thing the model knows."
            )

    def test_describe_tools(self, load):
        described = load("tools.py").describe_tools()
        assert "calculate:" in described
        assert len(described.strip().splitlines()) == 4


class TestChains:
    def test_prompt_has_the_role_and_the_variable(self, load):
        prompt = load("chains.py").build_prompt("translator")
        rendered = prompt.invoke({"question": "Hello?"})
        contents = " ".join(m.content for m in rendered.messages)
        assert "translator" in contents
        assert "Hello?" in contents

    def test_prompt_requires_its_variable(self, load):
        prompt = load("chains.py").build_prompt("translator")
        with pytest.raises(Exception):
            prompt.invoke({})

    def test_simple_chain_returns_a_string(self, load):
        model = FakeChat([ai("Bonjour")])
        chain = load("chains.py").simple_chain(model, "translator")
        result = chain.invoke({"question": "Hello?"})
        assert result == "Bonjour", (
            f"Got {result!r}. StrOutputParser turns the AIMessage into a plain "
            "string - without it you get the message object."
        )

    def test_ask(self, load):
        model = FakeChat([ai("Bonjour")])
        assert load("chains.py").ask(model, "translator", "Hello?") == "Bonjour"

    def test_ask_sends_the_system_role(self, load):
        model = FakeChat([ai("ok")])
        load("chains.py").ask(model, "pirate", "Hello?")
        sent = " ".join(m.content for m in model.last_call)
        assert "pirate" in sent

    def test_bound_model_knows_the_tools(self, load):
        model = FakeChat([ai("ok")])
        load("chains.py").bound_model(model)
        assert model.bound_tools is not None, "bind_tools was never called."
        assert len(model.bound_tools) == 4

    def test_tool_calls_for(self, load):
        model = FakeChat([ai_tool("calculate", {"expression": "2+2"}, id="t1")])
        calls = load("chains.py").tool_calls_for(model, "what is 2+2")
        assert calls[0]["name"] == "calculate"
        assert calls[0]["args"] == {"expression": "2+2"}

    def test_tool_calls_for_when_there_are_none(self, load):
        model = FakeChat([ai("Paris.")])
        assert load("chains.py").tool_calls_for(model, "capital?") == [], (
            "An empty tool_calls list is how LangChain says 'no tool wanted' - "
            "it replaces checking stop_reason."
        )

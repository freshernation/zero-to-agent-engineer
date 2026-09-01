# Day 1 — LangChain's pieces

> **By the end of today** you can use LangChain's messages, prompt templates, tools and
> output parsers — and say which of them are worth using.

Today is deliberately unexciting. It is a vocabulary lesson: the same ideas you already
have, with the names the ecosystem uses.

---

## Read / watch first

- [ ] [**LangChain core concepts**](../../content/week-08/day-1/langchain-core-concepts.md) — 30 min · docs: [LangChain — Introduction](https://python.langchain.com/docs/introduction/)

---

## What you need to know

### Messages are objects now

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

messages = [
    SystemMessage("You are terse."),
    HumanMessage("What is 2+2?"),
    AIMessage("4"),
]
```

Your `{"role": "user", "content": "..."}` dicts, as classes. That is genuinely all this
is. The advantage is that every LangChain component agrees on the type; the cost is one
more thing to import.

`ToolMessage(content="391", tool_call_id="t1")` is your `tool_result` block. Same three
fields, same rules — including that the id has to match.

### Prompt templates

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("human", "{question}"),
])

messages = prompt.invoke({"role": "translator", "question": "Hello in French?"})
```

An f-string with a schema attached. It validates that you supplied every variable,
which is a real convenience once a prompt has six of them and lives in another file.

For a one-off prompt in the same function, an f-string is still fine. Reach for a
template when the prompt is reused, configurable, or long enough to want to keep
somewhere else.

### `@tool`

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '2 + 2 * 3'."""
    return str(eval(expression, {"__builtins__": {}}, {}))
```

This is the first thing today that is a genuine saving. The decorator builds your
week-7 schema **from the type hints and the docstring**:

```python
calculate.name          # "calculate"
calculate.description   # the docstring
calculate.args          # {"expression": {"type": "string", ...}}
calculate.invoke({"expression": "17 * 23"})     # "391"
```

Everything you hand-wrote in `schemas.py` on Monday of week 7, generated. And notice
what it means: **the docstring is now the prompt.** The thing you were told mattered
most has been wired directly to the thing you write anyway.

### Binding tools

```python
model_with_tools = model.bind_tools([calculate, save_note])
response = model_with_tools.invoke(messages)

response.tool_calls     # [{"name": "calculate", "args": {...}, "id": "t1"}]
```

`response.tool_calls` is your `[b for b in content if b.type == "tool_use"]`, done for
you. A list of dicts rather than objects, and empty when the model did not ask for
anything — which is a slightly nicer check than `stop_reason`.

### LCEL — the `|` operator

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()
answer = chain.invoke({"role": "translator", "question": "Hello in French?"})
```

`|` means *feed the output of the left into the right*. The chain is a callable that
does all three steps.

It is neat, and it is the part of LangChain people argue about, because the tidiness
costs you the ability to put a `print` in the middle. Use it for genuinely linear
pipelines. When there is a decision in the middle, that is a graph, and graphs are
tomorrow.

---

## Exercises

```bash
pytest week-08/day-1 -v
```

### 1. `messages.py`

| Function | Returns |
|---|---|
| `to_langchain(messages)` | your week-6 dicts as LangChain message objects |
| `to_dicts(messages)` | the reverse |
| `describe(messages)` | `"system, human, ai"` — the types in order, lowercase |
| `last_ai_text(messages)` | the content of the last `AIMessage`, or `None` |

### 2. `tools.py`

Four tools, decorated with `@tool`, with **real docstrings**:

| Tool | Does |
|---|---|
| `calculate(expression)` | arithmetic; raises `ValueError("Unsafe expression")` for anything else |
| `word_count(text)` | how many words |
| `city_info(city)` | the sentence from week 7 |
| `reverse_text(text)` | the text backwards |

Plus:

| Function | Returns |
|---|---|
| `all_tools()` | the list of all four |
| `tool_by_name(name)` | one tool, or `None` |
| `describe_tools()` | `"calculate: Evaluate a basic..."` per line |

### 3. `chains.py`

| Function | Returns |
|---|---|
| `build_prompt(role)` | a `ChatPromptTemplate` with a `{question}` variable and the role in the system message |
| `simple_chain(model, role)` | `prompt \| model \| StrOutputParser()` |
| `ask(model, role, question)` | the answer as a plain string |
| `bound_model(model)` | the model with all four tools bound |
| `tool_calls_for(model, question)` | the `tool_calls` list from one bound call |

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 8 day 1" && git push
```

---

## Predict-then-run

Take your week-7 `schemas.py` — the hand-written dicts — and print
`calculate.args_schema.model_json_schema()` from today's `@tool` version next to it.

How close are they? What did the decorator get from your type hints, and what did it get
from your docstring? That comparison is the honest answer to "what does this framework
actually do", and you should be able to give it on Friday.

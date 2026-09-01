# Day 1 — Tools are a schema and a dictionary

> **By the end of today** you can describe a function to a model, receive its request
> to call one, and run it.

No loop yet. Today is one turn: you ask, it asks for a tool, you run the tool. Tomorrow
you put that in a `while`.

---

## Read / watch first

- [ ] [**Tool use / function calling**](../../content/week-07/day-1/tool-use.md) — 30 min · docs: [Tool use overview](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview)

---

## What you need to know

### A tool schema is a dict

```python
CALCULATE = {
    "name": "calculate",
    "description": "Evaluate a basic arithmetic expression like '2 + 2 * 3'.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic to evaluate.",
            },
        },
        "required": ["expression"],
    },
}
```

That is JSON Schema, and it is the whole interface. You send it in `tools=[...]`.

**The description is the prompt.** It is the only thing the model knows about your
function — not the code, not the name, not what you meant. A vague description produces
a tool that gets called at the wrong times with the wrong arguments, and the fix is
always in the description rather than in the code.

| Weak | Strong |
|---|---|
| "Gets weather" | "Return today's weather for a named city. Use only for current conditions, not forecasts." |
| "Does maths" | "Evaluate a basic arithmetic expression like '2 + 2 * 3'. Only + - * / and parentheses." |

Say what it does, when to use it, and — often most usefully — **when not to**.

### Sending them

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    tools=[CALCULATE, GET_WEATHER],
    messages=[{"role": "user", "content": "What is 17 * 23?"}],
)
```

### What comes back

```python
response.stop_reason        # "tool_use"  <- it wants something run
response.content            # [TextBlock("Let me work that out."), ToolUseBlock(...)]
```

A tool-use response often contains **both** — some text and the request. That is why
`content[0].text` finally breaks here, exactly as promised in week 6.

```python
for block in response.content:
    if block.type == "tool_use":
        block.name      # "calculate"
        block.input     # {"expression": "17 * 23"}
        block.id        # "toolu_01A..."  <- you must send this back
```

**The model has not run anything.** It produced JSON describing a call it would like
made. Running it is entirely your job, and that is the single most important sentence
of the week.

### Sending the result back

A tool result is an ordinary **user** message whose content is a list of blocks:

```python
messages.append(assistant_turn(response))       # what the model said, verbatim
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": block.id,        # matches the request
        "content": "391",               # always a string
    }],
})
```

Two things people get wrong:

- **The `tool_use_id` must match.** With several calls in flight, it is the only thing
  connecting an answer to its question.
- **You must resend the assistant turn too.** Skip it and the model sees a result for a
  request it has no record of making.

### A dispatch table

```python
TOOLS = {
    "calculate": calculate,
    "get_weather": get_weather,
}

result = TOOLS[block.name](**block.input)
```

A dict of name to function. `**block.input` unpacks the dict into keyword arguments.
That is the whole mechanism, and every framework you meet next week is wrapping this
dict.

`TOOLS[block.name]` raises `KeyError` for a name the model invented — which it will
occasionally do. Tomorrow you handle it; today, notice it can happen.

---

## Exercises

```bash
pytest week-07/day-1 -v
```

### 1. `tools.py` — three real functions

| Function | Returns |
|---|---|
| `calculate(expression)` | the result as a number; raises `ValueError("Unsafe expression")` for anything but digits, spaces, `+ - * / ( ) .` |
| `word_count(text)` | how many words |
| `city_info(city)` | `"Lisbon is in Portugal, population 545000."`, or `"I don't know about Narnia."` |

`CITIES` is given to you in the stub. **Do not `eval` unfiltered input** — check the
characters first. That check is the difference between a tool and a security incident,
and it is a real interview topic.

### 2. `schemas.py`

| Function | Returns |
|---|---|
| `make_schema(name, description, properties, required)` | a valid tool schema dict |
| `text_param(description)` | `{"type": "string", "description": ...}` |
| `all_schemas()` | a list of three schemas, one per tool above |

### 3. `dispatch.py`

| Function | Returns |
|---|---|
| `TOOLS` | the dispatch table — name to function |
| `run_tool(name, arguments)` | the result as a **string**; `"Unknown tool: xyz"` for a name that is not there |
| `tool_uses(response)` | the `tool_use` blocks, ignoring text |
| `handle_response(response)` | a list of `(tool_use_id, result_string)` for every call in it |

Everything comes back as a **string**, because that is what a `tool_result` block
carries. `391` and `"391"` are the same thing to the model.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 7 day 1" && git push
```

---

## Predict-then-run

You give the model a `get_weather` tool and ask *"What is the capital of France?"*

Does it call the tool? Should it? What in your schema decides?

Now change the description to *"Return today's weather for a city."* versus *"Look up
information about a city."* and ask the same question. **The description is the prompt**
— today's most useful five minutes is watching that be true.

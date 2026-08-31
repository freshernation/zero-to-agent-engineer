# Day 2 — The loop

> **By the end of today** you have written a working agent. All of it. No framework.

Yesterday's toolkit is given to you complete, in `toolkit.py`. Today the loop is the
only thing you build.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on the agent loop / ReAct pattern — 25 min]`

---

## What you need to know

### The loop, in full

```
messages = [the question]

repeat, up to a limit:
    response = model(messages, tools)

    if response.stop_reason != "tool_use":
        return the text            <- it is done

    messages.append(what the model just said)
    run every tool it asked for
    messages.append(the results, as a user message)

if the limit is reached:
    give up, and say so
```

Nine lines of English. Read it twice, then write it, and notice how little there is.
Every agent framework on earth is a wrapper around this.

### In Python

```python
messages = [{"role": "user", "content": question}]

for step in range(max_iterations):
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        tools=all_schemas(),
        messages=messages,
    )

    if response.stop_reason != "tool_use":
        return extract_text(response)

    messages.append(assistant_turn(response))

    results = []
    for block in tool_uses(response):
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": run_tool(block.name, block.input),
        })

    messages.append({"role": "user", "content": results})

return f"Stopped after {max_iterations} steps without finishing."
```

### Why `messages` grows

Every pass adds two entries: what the model said, and what the tools returned. The
model has no memory, so **the history is the agent's entire state**. There is nowhere
else anything is kept.

That has three consequences worth holding on to:

- A long agent run gets expensive fast — you resend everything, every step
- If you drop a turn, the model loses the thread completely
- "Agent memory" in any framework is a strategy for what to keep in this list

### `stop_reason` is the whole control flow

| Value | You do |
|---|---|
| `"tool_use"` | run the tools, go round again |
| `"end_turn"` | it has answered — return the text |
| `"max_tokens"` | it was cut off — your answer is incomplete |

That is the branch the entire loop turns on. Get it wrong and you either stop too early
or never stop at all.

### The iteration cap is not optional

A model can ask for a tool, get a result it does not like, and ask again. Forever. With
no cap you get an infinite loop that costs real money and is running while you sleep.

**Write the cap before you write anything else.** Every framework has one, every one of
them defaults to something small, and every production incident report about agents
mentions it.

### The trace

An agent that returns only its final answer is impossible to debug. Record what
happened as it happens:

```python
trace.append({
    "step": step + 1,
    "type": "tool_call",
    "name": block.name,
    "input": block.input,
    "result": result,
})
```

A trace is what week 11's observability tooling is showing you. Building one by hand
now means LangSmith will look like a nicer view of something you already have.

---

## Exercises

```bash
pytest week-07/day-2 -v
```

`toolkit.py` is given. Import from it — do not rewrite it.

### 1. `agent.py`

| Function | Returns |
|---|---|
| `tool_result_message(pairs)` | a user message dict with one `tool_result` block per `(id, result)` pair |
| `run(client, question, max_iterations=5)` | the final text |
| `iterations_used(client, question, max_iterations=5)` | how many model calls it took |
| `run_with_trace(client, question, max_iterations=5)` | `(final_text, trace)` |

On hitting the cap, `run` returns exactly:

```
Stopped after 5 steps without finishing.
```

A trace entry is a dict. Tool calls carry `step`, `type` (`"tool_call"`), `name`,
`input` and `result`. The final answer carries `step`, `type` (`"answer"`) and `text`.

### 2. `show.py`

| Function | Returns |
|---|---|
| `format_step(entry)` | one readable line for a trace entry |
| `format_trace(trace)` | the whole trace as a string, one line per entry |
| `tool_names(trace)` | every tool name called, in order, repeats included |
| `summarise(trace)` | `"3 steps, 2 tool calls (calculate, city_info)"` |

`format_step` for a tool call:

```
1. calculate({'expression': '17 * 23'}) -> 391
```

and for an answer:

```
2. answer: 17 * 23 is 391.
```

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 7 day 2" && git push
```

**Then do this, and do not skip it:** close your editor, take a piece of paper, and draw
the loop from memory. Boxes and arrows. If you cannot, you have typed it rather than
understood it — and Friday's first question is exactly this, on paper, with no laptop.

---

## Predict-then-run

Script a fake client to return `tool_use` **every single time**, and run your agent with
`max_iterations=5`.

How many model calls happen? How many tool calls? What does it return? And — the real
question — what would that have cost against a real API at $3 per million input tokens,
with the history growing every step?

That is why the cap is the first line you write.

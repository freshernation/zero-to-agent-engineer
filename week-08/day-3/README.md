# Day 3 — The port

> **By the end of today** last week's agent runs as a LangGraph graph, and you can point
> at what moved where.

The most valuable day of the week. You are not learning a new idea — you are watching
one you already own get rearranged, and noticing exactly what changes.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on building an agent in LangGraph — 30 min]`

---

## Your week-7 loop, mapped

| Week 7 | Week 8 |
|---|---|
| `messages` list you appended to | the graph's **state**, with an `add_messages` reducer |
| "call the model" | a **node** |
| "run the tools" | a **node** |
| `if response.stop_reason != "tool_use"` | a **conditional edge** |
| `for step in range(max_iterations)` | a step counter in the state, checked in the router |
| `assistant_turn(response)` | the reducer, automatically |
| matching `tool_use_id` | `ToolMessage(tool_call_id=...)`, still by hand |
| your `trace` list | the message list itself |

Two of those are genuine savings — the reducer, and not writing the loop's plumbing.
The rest is the same work with different names. Keep this table; Friday asks you to
defend every row.

---

## What you need to know

### State for an agent

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    steps: int
```

`add_messages` is the reducer built for this. It appends, and it handles a message
being updated by id rather than duplicated. A node returning `{"messages": [reply]}`
adds one message — it does not replace the history, which is what `operator.add` on a
plain list would also do but with fewer safeguards.

### The model node

```python
def call_model(state: AgentState) -> dict:
    response = model.bind_tools(all_tools()).invoke(state["messages"])
    return {"messages": [response], "steps": state["steps"] + 1}
```

The whole of week 7's "send the history, get a reply, append it". The appending is the
reducer's job now.

### The tools node

```python
def run_tools(state: AgentState) -> dict:
    last = state["messages"][-1]
    results = []
    for call in last.tool_calls:
        tool_function = tool_by_name(call["name"])
        if tool_function is None:
            content = f"Unknown tool: {call['name']}"
        else:
            try:
                content = str(tool_function.invoke(call["args"]))
            except Exception as error:
                content = f"Tool failed: {error}"
        results.append(ToolMessage(content=content, tool_call_id=call["id"]))
    return {"messages": results}
```

Look closely at what did **not** change: you still look the tool up, you still run it,
you still catch its failure, and you still match the id by hand. The framework did not
take that away — it took away the message plumbing around it.

`ToolMessage(tool_call_id=...)` is your `tool_result` block. Same id, same rule, same
bug if you get it wrong.

### The router

```python
def route(state: AgentState) -> str:
    if state["steps"] >= MAX_STEPS:
        return END
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return END
```

Your `if stop_reason != "tool_use"`, plus the cap. **The cap is still yours.** LangGraph
has a `recursion_limit`, but it raises an exception rather than ending cleanly, and a
production agent wants to finish with an answer rather than a stack trace.

### Wiring it

```python
graph = StateGraph(AgentState)
graph.add_node("model", call_model)
graph.add_node("tools", run_tools)
graph.add_edge(START, "model")
graph.add_conditional_edges("model", route, ["tools", END])
graph.add_edge("tools", "model")        # <- the loop
app = graph.compile()
```

That `add_edge("tools", "model")` is the whole cycle. One line, and it is the same
`while` you wrote last week.

---

## Exercises

```bash
pytest week-08/day-3 -v
```

`toolkit.py` is given — Monday's tools, complete.

### `agent_graph.py`

| Thing | Does |
|---|---|
| `AgentState` | `messages` (with `add_messages`) and `steps: int` |
| `make_call_model(model)` | returns the model node for that model |
| `run_tools(state)` | the tools node — returns one `ToolMessage` per call |
| `make_route(max_steps)` | returns the router |
| `build_agent(model, max_steps=6)` | the compiled graph |
| `run(model, question, max_steps=6)` | the final text |
| `run_with_state(model, question, max_steps=6)` | `(final_text, final_state)` |

`make_call_model` and `make_route` return functions because a node takes only the
state — anything else it needs has to be closed over. That is a real pattern and worth
recognising.

On hitting the cap, `run` returns the last text it has, or
`"Stopped after 6 steps without finishing."` if there is none.

`run_tools` must handle an unknown tool and a tool that raises, exactly as last week:
the result is a `ToolMessage` either way, and the graph carries on.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 8 day 3: agent ported" && git push
```

**Then, while it is fresh:** open week 7's `agent.py` and today's `agent_graph.py` side
by side and write down three things that got shorter and two that did not. That list is
half of Friday's comparison and it is much harder to write on Thursday.

---

## Predict-then-run

Delete the step counter and the `state["steps"] >= MAX_STEPS` check, then run the agent
against a model scripted to ask for a tool every time.

What stops it? What does the error look like? Is that what you would want a customer to
see? The answer is why the cap stayed yours.

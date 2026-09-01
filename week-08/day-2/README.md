# Day 2 — Graphs

> **By the end of today** you can build a graph with state, nodes, and a decision in
> the middle — and say what it does that a `while` loop does not.

No model today. Just the machinery, on plain numbers, so the graph is the only thing
you are thinking about.

---

## Read / watch first

- [ ] [**LangGraph state and nodes**](../../content/week-08/day-2/langgraph-state-and-nodes.md) — 30 min · docs: [Graph API concepts](https://langchain-ai.github.io/langgraph/concepts/low_level/)

---

## What you need to know

### The three parts

A LangGraph program is:

1. **State** — a dict, whose shape you declare
2. **Nodes** — functions that take the state and return *part* of a new one
3. **Edges** — what runs next, sometimes conditionally

That is it. Your week-7 loop had all three too: `messages` was the state, "call the
model" and "run the tools" were the nodes, and the `if stop_reason` was the edge.

### State

```python
from typing import Annotated, TypedDict
import operator

class CounterState(TypedDict):
    count: int
    limit: int
    log: Annotated[list, operator.add]
```

`TypedDict` declares the keys. The interesting part is `Annotated[list, operator.add]`,
which is a **reducer**: it says *when a node returns a `log`, add it to the existing one
rather than replacing it.*

Without a reducer, an update **overwrites**. With `operator.add`, it accumulates. That
one distinction is most of what confuses people about LangGraph state, and it is worth
being able to say out loud:

> **A key without a reducer is last-write-wins. A key with one is merged by that
> function.**

For messages there is a purpose-built reducer, `add_messages`, which appends and also
handles updating a message by id. You meet it tomorrow.

### Nodes

```python
def increment(state: CounterState) -> dict:
    return {"count": state["count"] + 1, "log": ["incremented"]}
```

A node takes the whole state and returns a **partial** update. Keys you do not mention
are left alone. Returning `{"log": ["incremented"]}` appends one entry — the reducer
does the merging.

Nodes are ordinary functions. They are testable on their own, without a graph, and you
should test them that way.

### Edges

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(CounterState)
graph.add_node("increment", increment)
graph.add_node("double", double)

graph.add_edge(START, "increment")
graph.add_edge("increment", "double")
graph.add_edge("double", END)

app = graph.compile()
app.invoke({"count": 0, "limit": 5, "log": []})
```

`START` and `END` are the entry and exit. `compile()` checks the graph is wired up and
gives you something you can call.

### Conditional edges — the whole point

```python
def route(state: CounterState) -> str:
    if state["count"] < state["limit"]:
        return "increment"
    return END

graph.add_conditional_edges("increment", route, ["increment", END])
```

The routing function returns **the name of the next node**. Returning the node you just
came from is a loop, and that is how a graph does what your `while` did.

The third argument lists the possible destinations. It is optional and worth supplying:
it lets the graph be drawn, and it catches a typo in a returned name at build time
rather than at run time.

### So what does this buy you over a `while` loop?

An honest answer, which you will need on Friday:

| A graph gives you | A `while` loop gives you |
|---|---|
| a structure something else can inspect, draw, and resume | code you can read top to bottom |
| state merging you declare once instead of writing everywhere | no reducer concept to learn |
| a natural place to add persistence and interrupts (week 10) | fewer moving parts |
| conventions a team already knows | no dependency |

For today's counter, the `while` loop wins easily. The graph starts paying when you want
persistence, human approval mid-run, or a diagram — and it stops paying when you cannot
work out why a node ran twice.

Say that out loud on Friday and you will sound like someone who has used both.

---

## Exercises

```bash
pytest week-08/day-2 -v
```

### 1. `state.py`

**`CounterState`** — `count: int`, `limit: int`, and `log`, which **accumulates**.

| Function | Returns |
|---|---|
| `increment(state)` | `count` plus one, and `"incremented"` on the log |
| `double(state)` | `count` doubled, and `"doubled"` on the log |
| `is_even(state)` | `True` if `count` is even |
| `route_by_parity(state)` | `"double"` when even, `END` when not |
| `route_until_limit(state)` | `"increment"` while `count < limit`, `END` otherwise |

### 2. `graphs.py`

| Function | Builds |
|---|---|
| `build_linear()` | START → increment → double → END |
| `build_branching()` | START → increment → *(even?)* → double → END, or straight to END |
| `build_loop()` | START → increment → *(under the limit?)* → back to increment, else END |

Each returns a **compiled** graph. `initial(count=0, limit=5)` returns a starting state.

`build_loop()` from `count=0, limit=3` must end at `count == 3` with three log entries.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 8 day 2" && git push
```

Tomorrow you port the agent. Read `day-3/README.md` tonight.

---

## Predict-then-run

Remove the `Annotated[list, operator.add]` from `log` — make it a plain `list` — and run
`build_loop()` again.

What is in the log at the end, and why? Then put it back. That five-second experiment is
the clearest explanation of reducers you will ever get.

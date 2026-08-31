# Day 4 — Seeing inside, and debugging a graph

> **By the end of today** you can watch a graph run step by step, and find a bug in one.

A graph is harder to debug than a loop, because you cannot put a `print` in the middle
of an edge. What you get instead is streaming and inspection — and they are better,
once you know they exist.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on streaming and debugging LangGraph — 20 min]`

---

## What you need to know

### `stream` — one update per node

```python
for update in app.stream(initial_state):
    print(update)
```

`invoke` gives you the final state. `stream` gives you a dict per node as it finishes:

```python
{"model": {"messages": [AIMessage(...)], "steps": 1}}
{"tools": {"messages": [ToolMessage(...)]}}
{"model": {"messages": [AIMessage("It is 391.")], "steps": 2}}
```

The key is the node's name and the value is what it returned. **This is your week-7
trace**, produced by the framework rather than appended by hand — which is the single
clearest thing the framework bought you, and worth saying that way on Friday.

There are other stream modes (`"values"` gives the whole state each time,
`"messages"` streams tokens). `"updates"` — the default above — is the one for
debugging.

### Drawing it

```python
print(app.get_graph().draw_ascii())
```

A picture of the wiring, from the graph itself. Genuinely useful when a graph has grown
past six nodes, and a good thing to paste into a pull request.

### Where graph bugs live

| Symptom | Nearly always |
|---|---|
| a node runs twice | two edges point at it |
| state resets between nodes | a key with no reducer, being overwritten |
| the graph never ends | a router that never returns `END` |
| `KeyError` on the state | a node returned a key you did not declare |
| a router raises | it returned a node name that does not exist |

The last one is why the destination list — the third argument to
`add_conditional_edges` — is worth supplying: it turns a runtime surprise into a
build-time error.

---

## Exercises

```bash
pytest week-08/day-4 -v
```

### 1. `inspect_graph.py`

| Function | Returns |
|---|---|
| `node_updates(app, state)` | the list of `(node_name, update)` pairs from streaming |
| `node_sequence(app, state)` | just the node names, in order, repeats included |
| `count_visits(app, state, node)` | how many times one node ran |
| `final_state(app, state)` | the state after the last update |

`node_sequence` for a one-tool run is `["model", "tools", "model"]`. That list *is* the
trace, and you did not write it.

---

## Debugging, round eight

Three graph bugs.

| File | Should print |
|---|---|
| `broken_1.py` | `Log: ['a', 'b']` |
| `broken_2.py` | `Visits: 3` |
| `broken_3.py` | `Answer: It is 391.` |

- **`broken_1.py`** loses half its log. The state is declared wrong.
- **`broken_2.py`** runs a node one time too many. The router is checked *after*
  the node has already run — which changes what the condition should say.
- **`broken_3.py`** never gets the tool result back to the model. The wiring is one edge
  short.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 8 day 4" && git push
```

Tomorrow: both agents side by side, and the comparison. **Write the comparison notes
tonight while both are fresh** — it is much harder from memory.

---

## Predict-then-run

Run your day-3 agent with `stream` and print each update, next to your week-7 agent's
`trace`.

They contain the same information. One you wrote thirty lines to produce; the other
came free. Now ask the harder question: which one would you rather have when something
goes wrong at 3am, and why? There is a real answer either way and Friday wants yours.

# Day 1 — Persistence

> **By the end of today** a graph can be interrupted, restarted, and picked up where it
> left off.

This is the strongest argument for LangGraph you will see all course. It is genuinely
hard to build by hand and nearly free here.

---

## Read / watch first

- [ ] [**LangGraph checkpointers and threads**](../../content/week-10/day-1/langgraph-checkpointers.md) — 25 min · docs: [Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)

---

## What you need to know

### The problem

Your week-7 agent lived entirely in memory. Restart the process and the run is gone —
the message list, the step count, everything. For a chat that is fine. For an agent
that runs for four minutes across six tool calls, or one that has to wait for a person,
it is not.

### A checkpointer saves state after every node

```python
from langgraph.checkpoint.memory import MemorySaver

app = graph.compile(checkpointer=MemorySaver())
```

That is the whole change. Every node's update is now saved as a **checkpoint**, and the
run can be resumed from any of them.

`MemorySaver` keeps them in memory, which survives nothing — it is for learning and for
tests. Real deployments use `SqliteSaver` or `PostgresSaver`, and **the code above is
identical either way**. Swapping the storage is a one-line change, which is exactly the
kind of decision a framework should make cheap.

### Threads

```python
config = {"configurable": {"thread_id": "user-42"}}
app.invoke({"count": 0, "log": []}, config)
```

A `thread_id` names one conversation or one run. Every checkpoint belongs to a thread,
and threads are independent — two users, two ids, no interference.

Invoking again **with the same thread id continues that thread** rather than starting
over. That catches people out: the state you pass in is merged into what is already
saved, not substituted for it.

### Reading the state back

```python
snapshot = app.get_state(config)
snapshot.values        # the state right now
snapshot.next          # which node would run next - empty when finished
```

`snapshot.next` is how you tell a finished run from a paused one, and it is tomorrow's
whole mechanism.

### The history

```python
list(app.get_state_history(config))     # newest first
```

Every checkpoint of the thread. This is a **time machine**: you can look at what the
state was three nodes ago, and — with `update_state` — carry on from there with
something changed.

That last part is worth pausing on. Rewinding a run, changing one value, and continuing
is a genuinely powerful debugging tool, and it is the thing your hand-written loop could
never do without you building a whole state-saving layer yourself.

### Editing state

```python
app.update_state(config, {"count": 99})
```

Writes a new checkpoint with your changes merged in, honouring the reducers. Used for
correcting an agent mid-run, and for tomorrow's "the human said no" case.

---

## Exercises

```bash
pytest week-10/day-1 -v
```

### `persistence.py`

The counter graph from week 8, with saving.

| Function | Returns |
|---|---|
| `build(checkpointer=None)` | the compiled counter graph — `START → increment → (under limit?) → increment, else END` |
| `make_saver()` | a `MemorySaver` |
| `config_for(thread_id)` | `{"configurable": {"thread_id": ...}}` |
| `run(app, thread_id, count=0, limit=3)` | the final state |
| `state_of(app, thread_id)` | the values, or `None` if the thread has never run |
| `checkpoint_count(app, thread_id)` | how many checkpoints the thread has |
| `set_state(app, thread_id, updates)` | apply an update, return the new values |

`build()` with no checkpointer must still work — a graph that cannot run without
persistence is a graph that has made persistence compulsory, and that is a worse
default than it sounds.

Two threads must not see each other's state. There is a test.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 10 day 1" && git push
```

---

## Predict-then-run

Run a thread to completion. Then invoke it **again with the same thread id and the same
starting state**.

What does the log contain? Most people expect a fresh run and get something else
entirely. Once you can explain it, you understand what a thread is.

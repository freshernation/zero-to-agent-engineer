# Day 2 — Asking a human, and graphs inside graphs

> **By the end of today** a graph can stop and wait for a person, and a piece of a graph
> can be built and tested on its own.

Yesterday's persistence is what makes today possible. A graph that cannot save its state
cannot pause — it can only block, which is a completely different and much worse thing.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on human-in-the-loop with LangGraph — 25 min]`

---

## What you need to know

### Pausing

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["spend"],
)
```

The graph runs up to that node, saves, and **returns**. The process is free. Hours or
days later:

```python
app.invoke(None, config)     # None means "carry on from where you were"
```

Passing `None` rather than a state is the signal to resume. The state is already saved;
there is nothing to pass.

`interrupt_after` does the same on the other side of a node, for when you want to review
what it produced rather than approve what it is about to do.

### Why this needs a checkpointer

Without one there is nothing to come back to. A pause without persistence is a blocked
thread: it holds a process open, it does not survive a restart, and it cannot be resumed
by a different machine.

**That distinction is the strongest argument for a framework you will meet.** Your week-7
loop could have had an `input()` in the middle of the tool dispatch — and it would have
held the process open, died on restart, and been unresumable. Being able to say that
sentence is worth more than knowing the API.

### Finding out where it stopped

```python
snapshot = app.get_state(config)
snapshot.next       # ("spend",) when paused, () when finished
```

`next` is how you tell a paused run from a finished one. A finished thread has nothing
next.

### Saying no

Resuming runs the node. To *refuse*, change the state first and let the node see it:

```python
app.update_state(config, {"approved": False})
app.invoke(None, config)        # the node runs, sees the refusal, and does nothing
```

The node has to be written to check. That is a design decision worth noticing: the graph
gives you the pause, and **what "no" means is yours to define.**

### Subgraphs

A compiled graph can be a node in another graph:

```python
parent.add_node("child", child_graph)
```

Worth doing when a piece of the process is reused, or is complicated enough to want its
own tests. Not worth doing to make a diagram look tidier.

> **The gotcha, and it is a good one:** a subgraph returns its **whole state**, not just
> what its nodes changed. So a key with an accumulating reducer that the child merely
> *received* gets added to the parent's copy all over again — and you get it twice,
> whatever the child's nodes returned. The fix is to give the child its own state
> schema containing only the keys it actually needs. It is a genuinely confusing hour
> if you meet it by accident.

---

## Exercises

```bash
pytest week-10/day-2 -v
```

### 1. `approval.py`

An expense graph: `prepare → spend`, pausing before `spend`.

State: `amount: int`, `approved` (`None`, `True` or `False`), `log` (accumulating).

| Function | Does |
|---|---|
| `build(checkpointer)` | compiled, pausing before `spend` |
| `start(app, thread_id, amount)` | run until it pauses, return the state |
| `pending(app, thread_id)` | the node it is waiting on, or `None` if finished |
| `approve(app, thread_id)` | resume; the spend happens |
| `reject(app, thread_id)` | set `approved` to `False`, resume; the spend does not |
| `is_finished(app, thread_id)` | `True` when nothing is next |

`prepare` logs `"prepared 500"`. `spend` logs `"spent 500"` — or `"rejected"` when
`approved` is `False`.

### 2. `nested.py`

| Function | Does |
|---|---|
| `build_child()` | compiled: doubles `value` |
| `build_parent()` | compiled: adds one to `value`, then runs the child |
| `run_parent(value)` | the final state |

`run_parent(3)` gives `value == 8` — add one, then double. The child must be **the same
compiled graph** `build_child()` returns, used as a node, and it must be testable on its
own.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 10 day 2" && git push
```

---

## Predict-then-run

Start an approval thread and leave it paused. Now call `app.get_state(config)` and print
`.values` and `.next`.

Then imagine the process restarts. With `MemorySaver`, the state is gone. With
`SqliteSaver`, it is not — and the same two lines of code work.

Write down, in one sentence, what that means for an agent that has to wait for somebody
to come back from lunch. That sentence is the answer to "why not just use a while loop".

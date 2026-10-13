# Day 1 — A worker is a function

> **By the end of today** an agent you wrote is something another agent can call: a
> brief goes in, a report comes out, and nothing else crosses.

---

## Read / watch first

- [ ] [**An agent as a tool**](../../content/week-11/day-1/agent-as-a-tool.md) — 20 min · docs: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [ ] `agent_kit.py`, one folder up — 10 min. It is week 7's loop. Find the cap, the
  dispatch table, and where the tool result goes back.

---

## What you need to know

### An agent with a signature

Week 7's agent took a question and gave back text. Put that behind a function and you
have a worker:

```python
result = run_worker(researcher, "Find the population of Lisbon. Digits only.")
report(result)        # "545000"
```

To whoever calls it, it is a function that takes a string and returns a string. That
it loops, calls a model three times and uses a tool is its own business.

### What makes one worker different from another

Four things, and you choose all of them:

| | |
|---|---|
| **its system prompt** | what it is for |
| **its tools** | what it is able to do — and so what it is *not* able to do |
| **its model** | cheap or capable; each worker has its own client |
| **its description** | what an orchestrator reads when deciding whether to ask it |

The description is week 7's lesson again: **the description is the prompt.** An
orchestrator chooses a worker the same way a model chooses a tool, from that text and
nothing else.

### It starts from nothing, every time

```python
run_worker(researcher, "Population of Lisbon.")
run_worker(researcher, "And the one before?")     # it has no idea what you mean
```

Each brief opens an empty conversation. The worker does not remember the last brief,
and it never sees the conversation of whoever asked.

That is the feature — its context stays small and clean — and it is the cost. Tomorrow
is about the cost.

### How a worker looks to an orchestrator

Like any other tool: a name, a description, and one argument.

```python
{
    "name": "ask_researcher",
    "description": "Finds population figures for cities. ...",
    "input_schema": {
        "type": "object",
        "properties": {"brief": {"type": "string", "description": "..."}},
        "required": ["brief"],
    },
}
```

### A worker that did not finish must say so

A worker that hits its step cap still returns text: *"Stopped after 6 steps without
finishing."* Hand that back as it is and the orchestrator will read it as the answer.

So the report marks it: `Worker researcher did not finish: Stopped after 6 steps...`.
The reader has to be able to tell an answer from a failure.

---

## Exercises

```bash
pytest week-11/day-1 -v
```

### `worker.py`

| Function | Does |
|---|---|
| `make_worker(name, description, system, schemas, tools, client)` | a dict with those six keys |
| `worker_schema(worker)` | the tool schema: `ask_<name>`, the worker's description, one required string `brief` |
| `run_worker(worker, brief, max_steps=6)` | runs the worker's own agent on the brief, from an empty conversation; `run_agent`'s result plus `"worker": name` |
| `report(result)` | the worker's text when it answered; `Worker <name> did not finish: <text>` otherwise |

Describe the `brief` argument in a full sentence. The model that writes the brief has
to be told that the worker sees nothing else.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 1" && git push
```

---

## Predict-then-run

With a real key, make a researcher and brief it twice: first *"Population of Lisbon."*,
then *"Now double it."*

Predict what the second one says before you run it. Then read the reply and decide what
the second brief should have been.

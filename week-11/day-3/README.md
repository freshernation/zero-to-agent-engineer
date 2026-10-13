# Day 3 — The orchestrator

> **By the end of today** one agent hands work to two others, survives either of them
> failing, and tells you what the whole thing cost.

---

## Read / watch first

- [ ] [**Orchestrator and workers**](../../content/week-11/day-3/orchestrator-and-workers.md) — 25 min · docs: [Building effective agents — Orchestrator-workers](https://www.anthropic.com/engineering/building-effective-agents)

---

## What you need to know

### It is the loop you already have

```python
schemas = [worker_schema(w) for w in workers]
tools = {"ask_researcher": ..., "ask_analyst": ...}

run_agent(client, ORCHESTRATOR_SYSTEM, schemas, tools, question)
```

The orchestrator is `run_agent`. Its tools are functions that take a brief, run a
worker, and return the report. The model asks for `ask_researcher` exactly as it used
to ask for `calculate`.

### An orchestrator holds no tools of its own

It cannot look anything up. It cannot calculate. It can only ask.

Give it the real tools "to save a call" and it will use them, and you will have one
agent with two confused assistants. The split is the design.

### Its prompt has one job

Getting it to write a brief. Left alone it sends the worker four words. Its system
prompt has to say that a worker sees nothing but the brief — yesterday's lesson, now
written as an instruction.

### Three ways a delegation goes wrong

All three are your code's job, not the model's.

| What happens | What the orchestrator gets back |
|---|---|
| the worker ran out of steps | `Worker researcher did not finish: ...` — Monday's `report` |
| the worker's model raised | `Worker researcher failed: overloaded` — and the team carries on |
| the orchestrator will not stop delegating | `Refused: delegation limit of 4 reached.` — and the worker is **not run** |

A failure goes back as a string, the same as a failed tool did in week 7. The
orchestrator reads it and decides what to do. A team that crashes because one worker's
model was briefly down is a team nobody can run.

### Count everything

```python
result["model_calls"]    # {"orchestrator": 3, "researcher": 3, "analyst": 2}
result["total_calls"]    # 8
```

Eight model calls. Last week you estimated a number like this. Today you measure it,
and on Friday you put it next to what one agent needs.

---

## Exercises

```bash
pytest week-11/day-3 -v
```

`worker.py` is Monday's, given back to you.

### `team.py`

| Thing | Does |
|---|---|
| `ORCHESTRATOR_SYSTEM` | the orchestrator's instructions — it can only ask, and a worker sees only its brief |
| `run_team(client, question, workers, max_delegations=4, max_steps=8)` | runs it all |

`run_team` returns:

```python
{
    "text": str,                 # the orchestrator's final answer
    "stopped": str,              # "answered" or "cap"
    "delegations": [{"worker": ..., "brief": ..., "report": ...}, ...],
    "model_calls": {"orchestrator": n, "researcher": n, "analyst": n},
    "total_calls": int,
}
```

Every worker appears in `model_calls`, with 0 if it was never asked. Every delegation
appears in `delegations`, including the refused ones.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 3" && git push
```

---

## Predict-then-run

With a real key, ask your team *"How many people live in Lisbon and Bogota combined?"*
and print `result["delegations"]`.

Read the briefs the orchestrator wrote. Run each through Tuesday's `missing_parts`.
Then change one sentence of `ORCHESTRATOR_SYSTEM` and run it again.

That loop — read the briefs, change the prompt, read the briefs — is what tuning a
multi-agent system actually consists of.

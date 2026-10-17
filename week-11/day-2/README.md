# Day 2 — The handoff

> **By the end of today** you can write a brief a worker can act on, and put a number
> on what a handoff saves and what it loses.

---

## Read / watch first

- [ ] [**The brief and the report**](../../content/week-11/day-2/the-brief-and-the-report.md) — 25 min · docs: [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

---

## What you need to know

### What crosses is a string

When one agent asks another, two strings move: the brief going out, the report coming
back. Nothing else does.

The orchestrator may have read the user's whole request, three earlier reports and a
correction. The worker gets what is in the brief. Ask a model to delegate without
telling it this and it writes:

```
look up Lisbon
```

Look up *what* about Lisbon? In what form? Is anything already known? The worker will
guess, and it will guess confidently.

### A brief has three parts

```
Goal: Find the population of Lisbon.

What is known:
- The user wants a total for two cities
- Lagos is already done: 15400000

Return: The number, digits only.
```

- **Goal** — one task, stated so it could be handed to a stranger.
- **What is known** — so the worker does not redo it, or contradict it.
- **Return** — the form of the answer. Without it you get a paragraph when you needed
  a number.

Write it the way you would brief a contractor who has never seen the project, because
that is exactly what the worker is.

### What a handoff saves

The researcher made three model calls and read two tool results to produce one line.
All of that stayed in *its* context. The orchestrator's conversation grew by one line.

That is the real argument for a worker: **a long, messy piece of work is kept out of
the conversation that has to stay clear.** You can count it — the tokens the worker
used, minus the tokens it sent back.

### What a handoff loses

The same thing, seen from the other side. The researcher tried Porto, the lookup
failed, and its report said *"Lisbon: 545000."*

Nobody upstream will ever know there was a failure. Nothing crashed. The final answer
will simply be missing a city.

This is where multi-agent systems actually fail, and it is much harder to see than an
exception. So you check: which tool results did the worker see that are not in its
report?

### A budget per worker

Every report lands in the orchestrator's context, and that context is shared by all of
its workers. A worker that sends back a page leaves less room for everyone else — and
the orchestrator's own instructions, the task and its answer have to fit too.

So each worker gets a **share**: what is left of the window after a reserve for the
orchestrator, divided by the number of workers. A report over its share is cut — and
**says it was cut**, because a silently short report is exactly the lost fact above,
made worse. And a worker whose own conversation grew past its budget is named, even if
its report was short: it is the one that will start dropping things first.

---

## Exercises

```bash
pytest week-11/day-2 -v
```

### `brief.py`

| Function | Returns |
|---|---|
| `build_brief(goal, known, return_format)` | the three-part text above. `known` is a list; empty gives `- nothing yet`. `ValueError` for an empty goal or return format |
| `missing_parts(brief)` | which of `Goal`, `What is known`, `Return` do not start a line followed by a colon — in that order, any capitals |
| `estimate_tokens(text)` | `len(text) // 4` |
| `crossed(brief, report)` | tokens that crossed the handoff, both directions |
| `kept_out(result, report)` | the worker's input and output tokens, minus the report. Never below zero |
| `lost(result, report)` | the tool results in `result["tool_calls"]` that do not appear in the report |
| `report_budget(window, reserve, workers)` | `(window - reserve) // workers`. `ValueError` for no workers or a reserve that leaves nothing |
| `fit_report(report, budget)` | unchanged within budget; otherwise the first `budget * 4` characters and ` [cut: N characters over this worker's budget]` |
| `over_budget(results, budget)` | the worker names whose own `input_tokens` went above budget |

`missing_parts` is for checking a brief a **model** wrote. Tomorrow's orchestrator
writes its own.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 2" && git push
```

---

## Predict-then-run

Take a worker result where `lost` returns something. Now change the worker's system
prompt to *"Report every lookup you attempted, including the ones that failed."* and
run it again with a real key.

Did `lost` go to zero? And what happened to `kept_out`? Those two numbers pull against
each other, and choosing where to sit between them is most of what designing a handoff
is.

# Week 8 Milestone — Both Agents

> The same agent, twice, running side by side. Plus the comparison, which is the part
> that matters.

---

## The files

| File | Holds |
|---|---|
| `handwritten.py` | Your week-7 loop, against the Anthropic-shaped client |
| `graph_agent.py` | Wednesday's LangGraph version |
| `compare.py` | Runs both, counts the lines, checks they agree |
| `COMPARISON.md` | **The written comparison** |

Two given files you do not write: `tools_raw.py` (plain functions plus hand-written
schemas, for the hand-written agent) and `toolkit.py` (the same four tools with `@tool`).
Compare those two while you are here — that is one row of the table already done.

---

## `handwritten.py`

Week 7's agent, brought forward. Use `tools_raw.py`, and `FakeClient` from
`fake_model.py`.

| Function | Returns |
|---|---|
| `run(client, question, max_steps=6)` | the final text |
| `run_with_steps(client, question, max_steps=6)` | `(text, model_calls)` |

Same behaviour as week 7: unknown tools and failing tools come back as strings and the
loop carries on; the cap stops it with
`"Stopped after 6 steps without finishing."`

## `graph_agent.py`

Wednesday's version. Use `toolkit.py` and `FakeChat` from `fake_chat.py`.

| Function | Returns |
|---|---|
| `run(model, question, max_steps=6)` | the final text |
| `run_with_steps(model, question, max_steps=6)` | `(text, model_calls)` |

**The two must agree.** Given equivalent scripts, both return the same answer and take
the same number of model calls. There is a test for that, and it is the whole basis of
the comparison — two things that behave identically can be compared honestly.

## `compare.py`

| Function | Returns |
|---|---|
| `count_lines(path)` | lines of actual code — no blanks, no comment-only lines |
| `line_counts()` | `{"handwritten": N, "graph": M}` |
| `both_answers(client, model, question)` | `(handwritten_answer, graph_answer)` |
| `agree(client, model, question)` | `True` if both gave the same answer |

`line_counts()` gives you a real number for the comparison instead of a feeling.

---

## `COMPARISON.md` — the deliverable

Five sections. Write it from your own two files, with actual numbers.

| Section | What goes in it |
|---|---|
| `## What the framework removed` | Specific. Name the code you no longer write, and what does it instead. |
| `## What it did not` | Equally specific. The parts that look the same in both files. |
| `## Line counts` | The numbers from `line_counts()`, and whether the difference is as big as you expected. |
| `## Debugging` | Which was easier to debug, with an example from this week. |
| `## What I would choose` | For this agent, and for one that needed persistence and human approval. Different answers, defended. |

At least 400 words. It must mention **reducer**, **conditional edge**, and contain at
least one number. Those are not arbitrary: a comparison that never names the two things
the framework actually gave you was written from impressions rather than from the code.

> **This document is the reason week 7 existed.** Everybody applying for these jobs has
> used LangGraph. Almost nobody can say what it does, because almost nobody has written
> the thing it replaces.

---

## Check it

```bash
pytest week-08/milestone -v
```

Twenty-four tests.

---

## Ship it

```bash
git add -A && git commit -m "week 8 milestone: both agents and the comparison" && git push
```

Keep both agents in the repository permanently. The hand-written one is not dead code —
it is the evidence.

---

## Friday

The defence is mostly this document, read aloud and argued with.

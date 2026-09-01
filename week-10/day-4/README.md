# Day 4 — When several agents beat one, and when they do not

> **By the end of today** you can decide whether a problem needs more than one agent,
> and defend the answer either way.

---

## Read / watch first

- [ ] [**Multi-agent design trade-offs**](../../content/week-10/day-4/multi-agent-tradeoffs.md) — 20 min · docs: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

---

## What you need to know

### The default is one agent

One agent with five tools handles most things people build crews for. It is cheaper, it
is easier to debug, and there is nowhere for context to get lost between steps.

Start there. Add an agent when you can name the reason.

### The reasons that hold up

| Reason | Why it is real |
|---|---|
| **Different tools** | An agent with twenty tools chooses badly. Splitting the tool list splits the decision. |
| **Different permissions** | One agent may read customer data, another may send email. That boundary is a security control, not a design preference. |
| **Different models** | A cheap model for extraction, an expensive one for judgement. Real money. |
| **Genuinely parallel work** | Six independent lookups can run at once. |

### The reasons that do not

| Reason | Why not |
|---|---|
| "It mirrors how a team works" | Your org chart is not a system design. |
| "It is more modular" | So is a function. |
| "Specialised agents perform better" | Sometimes. Measure it before believing it. |
| "It is what the tutorial did" | The tutorial was demonstrating the tool. |

### The cost is not subtle

Every extra agent is at least one more model call, plus the tokens to hand context
across. A three-agent crew answering something a single agent handles in two calls might
take eight. That is four times the cost and four times the latency for the same answer.

**You can estimate this before writing any code**, and today you will.

### Context loss at the handoff

The sharpest technical objection. When agent A finishes and passes to agent B, what
crosses is **a string**. Everything A saw — the tool results, the intermediate
reasoning, the thing it decided was irrelevant — is gone.

If B needs any of that, it must re-fetch it, or A must have thought to include it. This
is where multi-agent systems actually fail in practice, and it is much harder to see
than a crash.

### How to decide, in one question

> *"What would break if one agent did all of this?"*

If the answer is "nothing, it would just be a longer tool list" — use one agent. If it
is "it would need permissions it should not have", or "it would be choosing between
twenty tools", you have your reason and you can say it out loud.

---

## Exercises

```bash
pytest week-10/day-4 -v
```

### 1. `decide.py`

Judgement, written down as code.

| Function | Returns |
|---|---|
| `REASONS` | the four reasons that hold up, as a list of strings |
| `assess(requirements)` | `{"recommend": "single"` or `"multi"`, `"reasons": [...]}` |
| `estimate_calls(agent_count, tools_used)` | a rough model-call count |
| `compare_designs(designs)` | `{name: estimated_calls}` |
| `cheapest(designs)` | the name of the cheapest |

`requirements` is a dict of flags: `different_tools`, `different_permissions`,
`different_models`, `parallel_subtasks`. Any one of them justifies more than one agent;
none of them means one. `reasons` lists only the flags that were actually set.

`estimate_calls` is `agent_count + tools_used` — one call per agent to decide, one more
per tool used to react to the result. Crude, and enough to notice a four-times
difference before writing anything.

---

## Debugging, round ten

| File | Should print |
|---|---|
| `broken_1.py` | `Log: ['prepared', 'spent']` |
| `broken_2.py` | `Alice: 3 steps  Bob: 2 steps` |
| `broken_3.py` | `Log: ['added', 'doubled']` |

- **`broken_1.py`** pauses and can never continue. The `invoke` itself looks fine — it
  stops halfway and says nothing. The complaint only arrives when you ask where it
  got to.
- **`broken_2.py`** gives two users the same state.
- **`broken_3.py`** has an entry in its log twice. It is yesterday's subgraph gotcha.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 10 day 4" && git push
```

---

## Predict-then-run

Take your week-7 agent and your day-3 crew, and estimate the model calls each needs for
*"what is the population of Lisbon, and how many digits is that"*.

Then answer the deciding question out loud: **what would break if one agent did all of
this?**

If you cannot name anything, you have your recommendation for tomorrow — and it is a
perfectly good one.

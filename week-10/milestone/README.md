# Week 10 Milestone — Two Designs, One Recommendation

> The same task built twice, and a written recommendation with numbers in it.

---

## The task

> *"What is the population of Lisbon, and how many digits is that number?"*

Two steps: look something up, then do arithmetic with what you found. Small enough to
build both ways in an afternoon, and big enough that the handoff between steps is real.

---

## The files

| File | Holds |
|---|---|
| `graph_version.py` | One LangGraph agent with both tools |
| `crew_version.py` | A CrewAI crew: two agents, two tasks |
| `analysis.py` | The cost estimates and the comparison |
| `RECOMMENDATION.md` | **The deliverable** |

Given to you: `toolkit.py` (LangChain tools) and `crew_tools.py` (the same tools in
CrewAI's shape).

---

## `graph_version.py`

| Function | Returns |
|---|---|
| `build(model, max_steps=6)` | the compiled agent graph |
| `run(model, question, max_steps=6)` | the final text |
| `run_with_steps(model, question, max_steps=6)` | `(text, model_calls)` |

Week 8's agent, unchanged in shape. One agent, both tools, a cap.

## `crew_version.py`

| Function | Returns |
|---|---|
| `make_researcher()` / `make_analyst()` | the two agents |
| `make_tasks(researcher, analyst)` | the two tasks, in order |
| `build_crew()` | the sequential crew |
| `describe(crew)` | `"2 agents, 2 tasks, sequential"` |

**Do not call `kickoff()` from a module the tests import.** Run it by hand once if you
have a key.

## `analysis.py`

| Function | Returns |
|---|---|
| `DESIGNS` | `{"single-agent": {...}, "crew": {...}}` — `agent_count` and `tools_used` |
| `estimate(design)` | `agent_count + tools_used` |
| `compare()` | `{name: estimate}` |
| `ratio()` | crew calls divided by single-agent calls, to 1dp |
| `recommend()` | `"single-agent"` or `"crew"`, and it should be the cheaper one **unless you can name a reason** |

---

## `RECOMMENDATION.md`

| Section | What goes in it |
|---|---|
| `## The task` | One paragraph. What it needs and why it takes two steps. |
| `## The two designs` | How each is put together. Be concrete. |
| `## What each costs` | The estimates, the ratio, and what that means in latency as well as money. |
| `## Where the crew would win` | Be fair to it. Name a task where it is the right answer. |
| `## My recommendation` | And the condition that would change it. |

At least 400 words, at least two numbers, and it must mention **context** — the handoff
between agents is a string, and everything the first one saw is gone. That is the
sharpest technical objection to multi-agent designs and a recommendation that skips it
was written from taste rather than reasoning.

> *"We tried it and it was not worth it"* is a perfectly good recommendation. It is also
> a more senior thing to say than *"we used CrewAI"* — rejecting a tool for a stated
> reason is the skill.

---

## Check it

```bash
pytest week-10/milestone -v
```

The graph version is run against a scripted model. The crew is checked structurally,
because running it costs money.

---

## Ship it

```bash
git add -A && git commit -m "week 10 milestone: two designs, one recommendation" && git push
```

---

## Friday

The defence is the recommendation, argued with — including the instructor taking the
opposite side of whichever one you chose.

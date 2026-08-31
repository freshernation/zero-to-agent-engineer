# Day 3 — CrewAI, and what its abstraction assumes

> **By the end of today** you can build a crew, and say what CrewAI decided for you.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on CrewAI basics — 30 min]`

---

## A note on running it

Building a crew needs no key. **Running one calls a real model and costs real money**,
so the tests only check that your crew is wired correctly — the roles, the tools, the
tasks, the order.

That is not a compromise. It is most of what there is to get right, and it is the same
distinction as every other week: the structure is yours, the model's answer is not.

If you have a key, run it for real once at the end. Watch the agents talk to each other.
Then look at how many model calls it took to answer something your week-7 agent answered
in two.

---

## What you need to know

### The model: agents, tasks, crews

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Researcher",
    goal="Find accurate facts about cities",
    backstory="You check things rather than remembering them.",
    tools=[city_info],
)

find = Task(
    description="Find the population of Lisbon.",
    expected_output="A single number",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[find], process=Process.sequential)
```

Three ideas:

- an **Agent** is a role, a goal, a backstory, and some tools
- a **Task** is a description, an expected output, and an agent to do it
- a **Crew** is agents plus tasks plus a process

`Process.sequential` runs the tasks in order, feeding each result to the next.

### The prompt is now a persona

`role`, `goal` and `backstory` are assembled into a system prompt for you. So the
backstory is not colour — **it is prompt engineering with a friendlier name**, and a
vague one produces a vague agent exactly as a vague system prompt did in week 6.

| Weak | Strong |
|---|---|
| "You are a helpful researcher." | "You check things rather than remembering them. You always use a tool when one exists, and say 'not found' rather than guessing." |

Everything you learned about system prompts applies unchanged. Only the field names
changed.

### `expected_output` is the output contract

Week 6's *"return only a JSON object with these keys"*, wearing a different name. It is
worth as much attention here as it was there, and for the same reason: it is what the
next task receives.

### What CrewAI decided for you

This is the day's real content. The abstraction is opinionated, and the opinions are:

| Decision | What it assumes |
|---|---|
| Tasks run in a fixed order | your work is a pipeline, not a loop |
| Each task's output feeds the next | the handoff is a string |
| Agents have personas | the model works better when told who it is |
| The loop is hidden | you will not need to see it |

**Every one of those is reasonable and none is free.** The last is the one to think
about hardest: your week-7 agent showed you every step, and here you get a result. When
something goes wrong you have `verbose=True` and a lot of scrolling.

### Where it is genuinely good

A linear pipeline of clearly different jobs — research, then draft, then edit — where
each stage wants a different persona and a different set of tools. That is what it is
built for and it does it in very little code.

### Where it is not

Anything that needs to loop, branch on a result, pause for a human, or survive a
restart. Those are Monday and Tuesday, and CrewAI does not offer them the same way.

---

## Exercises

```bash
pytest week-10/day-3 -v
```

The tests set a dummy `ANTHROPIC_API_KEY`, so construction works without a real one.

### 1. `crew_tools.py`

Three CrewAI tools with real docstrings:

| Tool | Does |
|---|---|
| `calculate(expression)` | arithmetic; `"Unsafe expression"` for anything else — returns the message, does not raise |
| `city_info(city)` | the sentence from week 7 |
| `word_count(text)` | how many words |

CrewAI tools return strings and should **not raise** — an exception inside a crew is
much harder to see than one in your own loop.

### 2. `crew_setup.py`

| Function | Returns |
|---|---|
| `make_researcher()` | an `Agent` with the `city_info` tool |
| `make_analyst()` | an `Agent` with `calculate` and `word_count` |
| `make_tasks(researcher, analyst)` | two `Task`s — find a fact, then do something with it |
| `build_crew()` | a sequential `Crew` with both agents and both tasks |
| `describe_crew(crew)` | `"2 agents (Researcher, Analyst), 2 tasks, sequential"` |

Every agent needs a `role`, a `goal`, and a `backstory` of at least twelve words. Every
task needs an `expected_output`. There are tests for both, and they exist because those
fields **are** the prompt.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 10 day 3" && git push
```

---

## Predict-then-run

Write down, before you look at anything: how many model calls do you think a two-task
crew makes to answer *"what is the population of Lisbon, and how many digits is that"*?

Now count how many your week-7 agent would take. (Two: one to ask for the tool, one to
answer. Possibly three.)

You do not need to run the crew to have an opinion, and the gap between your guess and
your agent's two is Friday's most interesting conversation.

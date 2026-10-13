# An agent as a tool

*Week 11 · Day 1 · about 20 minutes*

> By the end of this you can explain what a "sub-agent" is without using the word, and
> say what separates one worker from another.

---

## Read the official documentation first

| Page | What it gives you |
|---|---|
| [**Building effective agents**](https://www.anthropic.com/engineering/building-effective-agents) | Read the *Orchestrator-workers* section. Ten minutes. |

---

## There is no new mechanism

Sub-agent, worker, specialist, teammate. Every one of those words means the same
thing: **an agent that another agent can call.**

And you have called things from an agent since week 7. A tool is a function with a
schema. So wrap your agent in a function —

```python
def ask_researcher(brief: str) -> str:
    result = run_agent(client, RESEARCHER_SYSTEM, [LOOKUP_SCHEMA], LOOKUP_TOOLS, brief)
    return result["text"]
```

— describe it with a schema, and put it in another agent's dispatch table. That is a
multi-agent system. The calling agent cannot tell whether `ask_researcher` is three
model calls and a database, or one line of Python. It asked for a tool and got a
string.

---

## What a worker is made of

| | What it decides |
|---|---|
| **System prompt** | What the worker is for, and how it should report |
| **Tools** | What it can do. Equally: what it *cannot* |
| **Model** | Each worker has its own client, so each can use a different model |
| **Description** | Whether the calling agent ever asks it |

The first three shape the work. The fourth decides whether the work happens at all.
An orchestrator picks a worker exactly as a model picks a tool — by reading the
description. A worker described as *"helper"* gets asked for everything or for nothing.

Compare:

```
"Research assistant."

"Finds population figures for cities. Give it every city you need and say
 what form you want the numbers in. It cannot do arithmetic."
```

The second says what to send, what comes back, and what not to ask for. That last
clause saves a wasted call every time.

---

## A separate context

This is the property everything else this week follows from.

When you call a worker it opens **an empty conversation**. Its only message is the
brief. It does not see the user's question, the calling agent's history, or its own
previous briefs.

| Good | Bad |
|---|---|
| Its context is short, so it is cheap and it stays on task | It knows only what the brief says |
| Its mess — ten tool results, three dead ends — never reaches the caller | Whatever it leaves out of its report is gone |
| It cannot be confused by an unrelated earlier turn | It cannot be helped by a relevant one |

Tomorrow is entirely about the right-hand column.

---

## Failing out loud

Your week 7 loop returns a sentence when it hits its cap: *"Stopped after 6 steps
without finishing."* To a person that is obviously a failure. To a calling model it is
just the text the tool returned, and it may well build an answer on it.

So a worker's report distinguishes the two cases in the string itself:

```
545000
Worker researcher did not finish: Stopped after 6 steps without finishing.
```

The general rule, which you will use three more times this week: **anything that goes
wrong inside a worker comes back as a string the caller can read and act on** — never
as an exception, and never disguised as an answer.

---

## Check yourself

1. What is the difference between a tool and a worker, from the calling agent's side?
2. A worker is briefed twice. What does it remember from the first brief?
3. Why give two workers different tools rather than the same full set?

<details>
<summary>Answers</summary>

1. **None.** Both are a name, a description and a schema; both return a string. The
   difference is entirely in what happens behind the function.
2. **Nothing.** Each brief starts an empty conversation.
3. Because what a worker cannot do is part of its design. A researcher with no
   calculator cannot quietly do the analyst's job badly, and — Thursday — a worker that
   reads untrusted text and holds no dangerous tool cannot be talked into using one.
</details>

---

## What you can now do

- [ ] Explain a sub-agent as an agent behind a function signature
- [ ] Name the four things that make one worker different from another
- [ ] Write a worker description an orchestrator can choose from
- [ ] Say what a separate context buys and what it costs
- [ ] Make a worker's failure readable to whoever called it

**Next:** [The brief and the report](../day-2/the-brief-and-the-report.md) — the two
strings everything depends on.

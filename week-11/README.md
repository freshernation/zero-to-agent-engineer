# Week 11 — Several agents, by hand

> **Destination**
> An orchestrator that hands work to worker agents — each with its own context, its own
> tools and its own model — and a measurement that says whether it was worth it.

Last week you used a framework's idea of a team and estimated what it would cost. This
week you build one yourself, with no framework, and measure it.

---

## The whole idea, up front

You already wrote everything a team is made of.

A **worker** is week 7's agent with a function signature around it: a string goes in,
a string comes out. An **orchestrator** is week 7's agent whose tools happen to be
workers.

That is all there is. There is no new kind of loop this week. What is new is what
happens **between** the agents — and that is where multi-agent systems fail:

1. **The handoff is a string.** Everything the worker is not told, it does not know.
   Everything it does not report, nobody ever sees.
2. **Every agent costs model calls.** A question one agent answers in four calls took
   eight in Wednesday's tests.
3. **A team fails in more ways.** A worker can be down, stuck, or wrong, and the
   orchestrator carries on regardless.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Turn an agent into a worker: a function with a brief in and a report out |
| Tue | `day-2/` | Write a brief that carries what the worker needs, and count what a handoff loses |
| Wed | `day-3/` | Build the orchestrator, with limits, and see what a team costs |
| Thu | `day-4/` | Run workers side by side, and decide which worker may hold which tool |
| Fri | `milestone/` | The same task as one agent and as a team — **measured**, with a recommendation |

---

## Given to you

`agent_kit.py`, at the top of this week's folder: week 7's loop as one function,
`run_agent`, and two tools. Read it on Monday before anything else. It is forty lines
and you have written all of them before.

---

## Why by hand

Every framework has a multi-agent feature and each one hides the same three things:
what the worker was told, what it sent back, and how many calls it took. Build it once
with those three in plain sight and you can read any framework's version — and you can
say, with a number, when not to use it.

Read `FENCE.md`.

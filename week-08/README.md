# Week 8 — Frameworks, on your terms

> **Destination**
> Rebuild last week's agent in LangGraph, and be able to say precisely what the
> framework bought you and what it took away.

Last week you wrote the loop. This week you meet the tools that hide it — and because
you wrote it, they will look like conveniences rather than magic.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Use LangChain's pieces — messages, prompts, tools, LCEL |
| Tue | `day-2/` | Build a graph: state, nodes, edges, conditions |
| Wed | `day-3/` | **Port week 7's agent to LangGraph** |
| Thu | `day-4/` | See inside a running graph, and debug one |
| Fri | `milestone/` | Both agents, side by side, plus the comparison |

---

## What changes, and what does not

The thinking changes. Weeks 1–7 were about making things work; from here the code gets
easier and the decisions get harder. This week you will spend more time choosing
between two reasonable options than fixing errors — and being able to defend a choice
is a more senior skill than being able to make something run.

What does not change is how you test. `fake_chat.py` is week 6's `FakeClient` wearing
LangChain's shape: script the replies, record the calls, assert on what you sent.
**Testing an agent is the same problem whichever framework is on top**, and noticing
that is most of the point.

---

## The comparison is the deliverable

Both agents stay in the repo. Same task, both running, and a written comparison with
real numbers in it.

That document is worth more in an interview than either agent. "I used LangGraph" is
what everyone says. "I wrote it by hand first, then ported it, and here is what changed"
is what almost nobody says.

---

## Read `FENCE.md`

Particularly the part about `create_react_agent`, which builds the whole thing in four
lines and is fenced off for a reason worth understanding.

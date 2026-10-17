# Week 11 — Concept fence

## Allowed

**Everything from Weeks 1–7 and week 9**, plus:

- `agent_kit.run_agent` — week 7's loop, given to you
- A worker as a dict, and a tool schema that describes it
- A brief and a report as plain strings
- One orchestrator and its workers — **two levels, no deeper**
- `asyncio.gather` and `asyncio.to_thread`, on Thursday
- Counting model calls and estimating tokens, and a token budget per worker

## Not yet

**Any framework.** No LangGraph, no CrewAI, no AutoGen, no agent SDK — you used two of
them last week and you will again; this week is for seeing what they hide · workers
that ask other workers · agents that talk to each other directly rather than through
the orchestrator · shared memory between agents · MCP and agent-to-agent protocols ·
planners · agent benchmark leaderboards

---

## Why two levels and no deeper

An orchestrator and its workers is the pattern that is actually in production, and it
is the one whose costs you can still count on your fingers.

Every level you add multiplies the model calls and adds another place for a fact to be
dropped in a handoff. A worker that briefs its own workers is a team you can no longer
explain from the trace — and a system you cannot explain is one you cannot debug at
three in the morning.

If Friday's numbers say a second level would help, you will be able to say exactly
why. Almost always they say the opposite.

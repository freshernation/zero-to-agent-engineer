# Week 10 — Concept fence

## Allowed

**Everything from Weeks 1–9**, plus:

- **LangGraph persistence** — `MemorySaver`, `thread_id`, `get_state`,
  `get_state_history`, `update_state`, resuming with `invoke(None, config)`
- **Interrupts** — `interrupt_before`, `interrupt_after`
- **Subgraphs** — a compiled graph used as a node
- **CrewAI** — `Agent`, `Task`, `Crew`, `Process.sequential`
- Everything from week 8

## Not yet

AutoGen, Swarm, OpenAI Agents SDK, or framework number five · database-backed
checkpointers (`SqliteSaver`, `PostgresSaver`) — `MemorySaver` shows the idea ·
`Process.hierarchical` in CrewAI · agent benchmark leaderboards · anything announced
this month

---

## A word about the leaderboards

Every few weeks a new agent framework appears with a benchmark showing it is best. You
now have the only defence that works: you have written the loop by hand, ported it,
measured a system, and can therefore ask *"what does this do that mine does not, and how
would I know?"*

That question is worth more than knowing any particular framework, and it is what the
last three weeks were quietly for.

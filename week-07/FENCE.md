# Week 7 — Concept fence

## Allowed

**Everything from Weeks 1–6**, plus:

- `tools=` in the request, and tool schemas as plain dicts
- `stop_reason == "tool_use"`, `ToolUseBlock` (`.name`, `.input`, `.id`)
- `tool_result` content blocks in a user message
- A dispatch table — a dict mapping tool names to functions
- `inspect.signature` if you want it (not required anywhere)
- `asyncio` — `async def`, `await`, `asyncio.run`, `asyncio.gather` (Thursday only)

## Not yet

**Any framework.** No LangChain, no LangGraph, no CrewAI, no AutoGen, no `smolagents`,
no `openai-agents`. Not one. · Multi-agent anything · Vector stores and embeddings
(week 9) · Persistent memory stores · Planners · MCP · Agent benchmarks

---

## Why the fence is absolute this week

Everything you build this week has a framework that will do it for you in four lines.
You will meet those frameworks next Monday, and they will feel obvious — *because you
will have already written what they hide*.

That is the entire design of this course, and this is the week it pays off. A student
who reaches for LangGraph now saves three days and loses the only chance they will ever
get to understand what an agent actually is. In week 8 you port this week's agent to
LangGraph and write down what the framework bought and what it cost. You cannot write
that comparison if you never built the first one.

It is also the difference in an interview. Everybody has used an agent framework.
Almost nobody can draw the loop on a whiteboard.

If an AI offers you LangChain this week, tell it no. That is what `ai/tutor.md`'s fence
is for.

# Week 8 — Concept fence

## Allowed

**Everything from Weeks 1–7**, plus:

- **LangChain core** — `HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage`,
  `ChatPromptTemplate`, `@tool`, `StrOutputParser`, `PydanticOutputParser`,
  and LCEL's `|` composition
- **LangGraph** — `StateGraph`, `START`, `END`, `add_node`, `add_edge`,
  `add_conditional_edges`, `compile`, `invoke`, `stream`
- `TypedDict` and `Annotated` for state, `operator.add` and
  `langgraph.graph.message.add_messages` as reducers
- `ToolNode` and `tools_condition` from `langgraph.prebuilt`
- `langchain_anthropic.ChatAnthropic` (for the optional real run)

## Not yet

CrewAI, AutoGen (week 10) · LangGraph checkpointers and persistence (week 10) ·
human-in-the-loop interrupts (week 10) · subgraphs (week 10) · embeddings and vector
stores (week 9) · LangSmith (week 11) · `create_react_agent` — **you are porting your
own, not calling the one-liner**

---

## The one rule that makes this week worth anything

**You port week 7's agent. You do not replace it.**

Both versions stay in the repository, side by side, running the same task. On Friday you
write down what the framework bought you and what it cost, with line counts and specific
examples.

`langgraph.prebuilt.create_react_agent` builds a working agent in four lines. It is
fenced off, and the reason is not purity — it is that a comparison between *your loop*
and *a function you called* teaches nothing. The comparison that teaches is between your
loop and a graph **you wired yourself out of the same pieces**.

You will use `create_react_agent` in your career, probably often. You will use it
knowing exactly what it is doing, which is a completely different thing from using it
because it works.

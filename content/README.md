# Course content

The reading for every day of the course. One article per `Read / watch first` item, each
opening with a link to the official documentation for its topic, then the fundamentals
with worked examples and diagrams.

Every day README links here; these articles link on to the next. They are written to be
published as standalone pages — the diagrams are self-contained SVG files in each day's
`img/` folder, and every relative link resolves within this tree.

| | |
|---|---|
| **Articles** | 66 |
| **Diagrams** | 104 |
| **Weeks covered** | 1–12 |

Weeks 1–4 anchor on [docs.python.org/3.14](https://docs.python.org/3.14/). Later weeks
anchor on the official documentation for the tool in question — pytest, requests,
pydantic, Anthropic, LangChain, LangGraph, CrewAI, FastAPI — because Python's own
documentation does not cover those. Week 12 has no official source and says so.

---

## Week 1 — Code is not magic

**Day 1** · [Running Python, and `print()`](week-01/day-1/running-python-and-print.md) · [Strings and quotes](week-01/day-1/strings-and-quotes.md)

**Day 2** · [Variables and types](week-01/day-2/variables-and-types.md) · [`input()` and type conversion](week-01/day-2/input-and-type-conversion.md)

**Day 3** · [`if` / `elif` / `else`](week-01/day-3/if-elif-else.md) · [Boolean logic — `and`, `or`, `not`](week-01/day-3/boolean-logic.md)

**Day 4** · [Reading Python tracebacks](week-01/day-4/reading-python-tracebacks.md)

## Week 2 — Many things at once

**Day 1** · [Python lists](week-02/day-1/python-lists.md) · [Indexing and slicing](week-02/day-1/indexing-and-slicing.md)

**Day 2** · [`for` loops and `range`](week-02/day-2/for-loops-and-range.md) · [`while` loops](week-02/day-2/while-loops.md)

**Day 3** · [Python dictionaries](week-02/day-3/python-dictionaries.md) · [Nested data — lists of dicts](week-02/day-3/nested-data.md)

**Day 4** · [Tuples and sets](week-02/day-4/tuples-and-sets.md) · [Sorting in Python](week-02/day-4/sorting-in-python.md)

## Week 3 — Pieces, storage, failure

**Day 1** · [Defining and calling functions](week-03/day-1/defining-and-calling-functions.md) · [Return values and scope](week-03/day-1/return-values-and-scope.md)

**Day 2** · [`try` / `except`](week-03/day-2/try-except.md) · [Raising exceptions](week-03/day-2/raising-exceptions.md)

**Day 3** · [Reading and writing files](week-03/day-3/reading-and-writing-files.md) · [JSON in Python](week-03/day-3/json-in-python.md)

**Day 4** · [List comprehensions](week-03/day-4/list-comprehensions.md) · [`lambda` and `sorted(key=)`](week-03/day-4/lambda-and-sorted-key.md)

## Week 4 — Objects, tests, an audience

**Day 1** · [Python classes and `__init__`](week-04/day-1/classes-and-init.md) · [`self` and instance attributes](week-04/day-1/self-and-instance-attributes.md)

**Day 2** · [`__repr__` and `__eq__`](week-04/day-2/repr-and-eq.md) · [Composition](week-04/day-2/composition.md)

**Day 3** · [Writing tests with pytest](week-04/day-3/writing-tests-with-pytest.md) · [pytest fixtures and `parametrize`](week-04/day-3/pytest-fixtures-and-parametrize.md)

**Day 4** · [Python type hints](week-04/day-4/type-hints.md) · [Writing a good README](week-04/day-4/writing-a-good-readme.md)

## Week 5 — Talking to the internet

**Day 1** · [How HTTP works](week-05/day-1/how-http-works.md) · [The `requests` library](week-05/day-1/the-requests-library.md)

**Day 2** · [pydantic v2 basics](week-05/day-2/pydantic-basics.md) · [pydantic validators](week-05/day-2/pydantic-validators.md)

**Day 3** · [Environment variables and `.env` files](week-05/day-3/environment-variables.md) · [Retries and backoff](week-05/day-3/retries-and-backoff.md)

**Day 4** · [Combining API data](week-05/day-4/combining-api-data.md)

## Week 6 — Talking to a model

**Day 1** · [The Anthropic Messages API](week-06/day-1/anthropic-messages-api.md) · [Tokens and context windows](week-06/day-1/tokens-and-context-windows.md)

**Day 2** · [Prompt engineering fundamentals](week-06/day-2/prompt-engineering.md) · [Temperature and sampling](week-06/day-2/temperature-and-sampling.md)

**Day 3** · [Structured output from LLMs](week-06/day-3/structured-output.md)

**Day 4** · [Streaming responses](week-06/day-4/streaming-responses.md) · [Managing conversation context](week-06/day-4/managing-conversation-context.md)

## Week 7 — Build the agent

**Day 1** · [Tool use / function calling](week-07/day-1/tool-use.md)

**Day 2** · [The agent loop / ReAct pattern](week-07/day-2/agent-loop.md)

**Day 3** · [Agent failure modes](week-07/day-3/agent-failure-modes.md)

**Day 4** · [`asyncio` basics](week-07/day-4/asyncio-basics.md)

## Week 8 — Frameworks, on your terms

**Day 1** · [LangChain core concepts](week-08/day-1/langchain-core-concepts.md)

**Day 2** · [LangGraph state and nodes](week-08/day-2/langgraph-state-and-nodes.md)

**Day 3** · [Building an agent in LangGraph](week-08/day-3/agent-in-langgraph.md)

**Day 4** · [Streaming and debugging LangGraph](week-08/day-4/streaming-and-debugging.md)

## Week 9 — Retrieval, and proving it

**Day 1** · [Chunking strategies for RAG](week-09/day-1/chunking-strategies.md)

**Day 2** · [Embeddings and vector similarity](week-09/day-2/embeddings-and-similarity.md)

**Day 3** · [RAG prompt construction](week-09/day-3/rag-prompt-construction.md)

**Day 4** · [Evaluating retrieval](week-09/day-4/evaluating-retrieval.md)

## Week 10 — Multi-agent, and its cost

**Day 1** · [LangGraph checkpointers and threads](week-10/day-1/langgraph-checkpointers.md)

**Day 2** · [Human-in-the-loop with LangGraph](week-10/day-2/human-in-the-loop.md)

**Day 3** · [CrewAI basics](week-10/day-3/crewai-basics.md)

**Day 4** · [Multi-agent design trade-offs](week-10/day-4/multi-agent-tradeoffs.md)

## Week 11 — Put it where people can reach it

**Day 1** · [FastAPI basics](week-11/day-1/fastapi-basics.md)

**Day 2** · [Twelve-factor config and deployment](week-11/day-2/config-and-deployment.md)

**Day 3** · [Structured logging and tracing](week-11/day-3/logging-and-tracing.md)

**Day 4** · [LLM evaluation and guardrails](week-11/day-4/evaluation-and-guardrails.md)

## Week 12 — The interview is the deliverable

**Day 1** · [Résumés for career changers](week-12/day-1/resumes-for-career-changers.md)

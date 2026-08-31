# Week 6 — Concept fence

## Allowed

**Everything from Weeks 1–5**, plus:

- `anthropic` — `Anthropic()`, `client.messages.create(...)`, `client.messages.stream(...)`
- Request fields — `model`, `max_tokens`, `system`, `messages`, `temperature`,
  `stop_sequences`
- Response fields — `.content`, block `.type` and `.text`, `.stop_reason`,
  `.usage.input_tokens`, `.usage.output_tokens`, `.model`
- `anthropic.APIError`, `anthropic.RateLimitError`, `anthropic.APIStatusError`
- pydantic for parsing what the model returns
- `json.loads` and its `JSONDecodeError`

## Not yet

Tool calling and the agent loop (week 7) · LangChain, LangGraph, CrewAI (week 8) ·
embeddings and vector stores (week 9) · async streaming · batch API · files and
vision · prompt caching · fine-tuning · `tools=` in the request

---

## The rule that makes this week testable

**Every function you write takes a `client` argument.**

```python
def summarise(client, text):        # yes
def summarise(text):                # no - where does the client come from?
```

Real model calls cost money, need a key, and answer differently every time, so the
tests hand your functions a stand-in from `fake_model.py` instead.

That is not a testing trick. Passing in the thing your code depends on rather than
reaching for a global is **dependency injection**, it is how every serious codebase
handles anything external, and it is the reason your week-7 agent will be testable at
all. It is also a genuine interview topic.

---

## Running against the real thing

Optional, not graded, and worth doing once so the fake never feels like the whole story:

```bash
export ANTHROPIC_API_KEY=your-key-here
python3 week-06/try_it.py
```

The code you write for the tests works unchanged — `FakeClient` copies the real SDK's
shape exactly. That equivalence is the point: swap the object, keep the program.

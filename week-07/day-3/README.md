# Day 3 — When the agent misbehaves

> **By the end of today** your agent survives tools that fail, arguments that are
> wrong, names that do not exist, and its own tendency to go round in circles.

Yesterday's loop works when everything works. Today is the other 80% — and it is the
part that separates a demo from something you would leave running.

---

## Read / watch first

- [ ] [**Agent failure modes**](../../content/week-07/day-3/agent-failure-modes.md) — 20 min · docs: [Handling tool errors](https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use#handling-tool-errors)

---

## The five ways an agent goes wrong

### 1. It invents a tool

```python
ToolUseBlock("search_web", {"query": "..."})     # you never had that tool
```

Your dispatch table raises `KeyError`. **Do not let that crash the loop.** Send back
`"Unknown tool: search_web"` as the result — the model reads that, apologises, and
usually recovers. An agent that dies because the model guessed wrong is an agent that
cannot self-correct, which was the entire reason for the loop.

### 2. The arguments are wrong

```python
ToolUseBlock("calculate", {"expr": "2+2"})       # you called it "expression"
ToolUseBlock("calculate", {})                    # nothing at all
```

`function(**arguments)` raises `TypeError`. Same treatment: catch it, describe it, send
it back. *"missing required argument: expression"* is a message the model can act on.

### 3. The tool itself fails

Division by zero, a 404, a timeout. Your tool raises. The model needs to know what
happened, so it can try something else — or tell the user it could not.

**All three of these have the same fix:** every tool call returns a string, always.
Success or failure, the model gets an answer. A tool that raises into your loop has
broken the contract.

### 4. It goes round in circles

The genuinely hard one. The model calls `calculate("2+2")`, gets `4`, does not like it,
and calls `calculate("2+2")` again. And again. Every call is legal, nothing raises, and
the bill grows.

The iteration cap catches this eventually. **Repeat detection catches it in two steps
instead of five**, and it is cheap:

```python
signature = (block.name, json.dumps(block.input, sort_keys=True))
if seen.count(signature) >= max_repeats:
    stop
```

`sort_keys=True` matters — `{"a":1,"b":2}` and `{"b":2,"a":1}` are the same call, and
would not be if you compared the raw strings.

### 5. The context runs away

Every step adds the model's turn *and* the tool results. A tool that returns 50,000
characters of HTML puts all of it in the history, and it stays there for every
remaining step.

**Truncate tool results.** Five hundred characters and a marker is almost always enough
for the model to work with, and it stops one greedy tool ending the run.

---

## Why a class, now

Yesterday's functions each passed `client`, `max_iterations` and the trace around. That
is week 4's signal that these things belong together:

```python
class Agent:
    def __init__(self, client, max_iterations=5, max_repeats=2):
        ...
    def run(self, question):
        ...
```

State and the behaviour that acts on it, travelling together. The `trace` and the
`stop_reason` become attributes you can inspect after a run rather than return values
you have to thread through.

---

## Exercises

```bash
pytest week-07/day-3 -v
```

`toolkit.py` is given again.

### 1. `guards.py`

| Function | Returns |
|---|---|
| `call_signature(name, arguments)` | a stable string; argument order must not matter |
| `count_calls(signatures, name, arguments)` | how many times that exact call already appears |
| `is_repeating(signatures, name, arguments, limit=2)` | `True` when it has already happened `limit` times |
| `validate_arguments(schema, arguments)` | `(True, "")` or `(False, "missing required argument: expression")` |
| `truncate(text, max_chars=500)` | the text, or the first `max_chars` plus `"... [truncated]"` |

`validate_arguments` reports **missing required** arguments first, then **unexpected**
ones as `"unexpected argument: expr"`.

### 2. `robust.py`

**`Agent(client, max_iterations=5, max_repeats=2)`**

| Member | Does |
|---|---|
| `run(question)` | returns the final answer |
| `trace` | the record of the run, same shape as yesterday |
| `stop_reason` | `"answered"`, `"cap"` or `"looping"` |
| `model_calls` | how many times the model was called |

Behaviour it must have:

- an unknown tool returns `"Unknown tool: <name>"` as the result and the loop **carries on**
- a tool that raises returns `"Tool failed: <message>"` and the loop carries on
- results longer than 500 characters are truncated
- a call repeated `max_repeats` times stops the run with
  `"Stopped: the agent repeated the same tool call."`
- hitting the cap stops with `"Stopped after N steps without finishing."`

Every one of those is a decision. Write them down as you go — Friday asks you to defend
each.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 7 day 3" && git push
```

Read the milestone spec tonight. Tomorrow is short.

---

## Predict-then-run

An agent with a `max_iterations` of 10, whose model asks for the same tool every time,
against a tool returning 2,000 characters.

Roughly how many tokens are in the tenth request? You do not need to be exact — you
need to notice that it is not ten times the first one, it is much worse than that, and
to be able to say why.

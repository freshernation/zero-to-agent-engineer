# Day 1 — The Messages API

> **By the end of today** you can send a request to a model, get the text out of what
> comes back, and say what it cost.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on the Anthropic Messages API — 25 min]`
- [ ] `[INSTRUCTOR: source on tokens and context windows — 15 min]`

---

## What you need to know

### The call

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is a token?"}],
)
```

Four things, three of them required:

| Field | Does |
|---|---|
| `model` | which model |
| `max_tokens` | **required** — the cap on the *reply* length |
| `messages` | the conversation so far, as a list of dicts |
| `system` | optional — the standing instruction (see tomorrow) |

`max_tokens` is a **limit, not a target**. Set it to 1000 and a one-word answer still
costs you one word. Set it too low and your reply gets cut off mid-sentence, which you
detect by checking `stop_reason`.

### Messages are a list of dicts

Week 2 again:

```python
messages = [
    {"role": "user", "content": "What is a token?"},
    {"role": "assistant", "content": "A token is a chunk of text..."},
    {"role": "user", "content": "How many in a word?"},
]
```

Two roles: `user` and `assistant`. They must alternate, and the list must start with
`user`.

**The model has no memory.** It does not remember the earlier turns — you are resending
them, every single call. That is what a conversation *is*, and it is why long ones get
expensive.

### The response

```python
response.content            # a LIST of blocks, not a string
response.content[0].text    # the text of the first block
response.stop_reason        # "end_turn" | "max_tokens" | "stop_sequence"
response.usage.input_tokens
response.usage.output_tokens
response.model
```

`content` is a list because a response can contain several blocks — text, and from next
week, tool calls. Reaching straight for `content[0].text` works until the day it does
not, so the safe extraction is:

```python
text = "".join(block.text for block in response.content if block.type == "text")
```

### `stop_reason` — the field everyone ignores

| Value | Means |
|---|---|
| `end_turn` | it finished naturally |
| `max_tokens` | **it was cut off.** Your answer is incomplete |
| `stop_sequence` | it hit one of your stop strings |

A truncated answer looks like a real answer. It is a complete sentence, it is
plausible, and it is missing the end. **Check `stop_reason` before you use a response**
— it is this week's version of checking the status code.

### Tokens and cost

A token is roughly ¾ of a word in English. You pay for input and output separately, and
output usually costs several times more than input.

```python
def cost(usage, input_per_million, output_per_million):
    return (
        usage.input_tokens / 1_000_000 * input_per_million
        + usage.output_tokens / 1_000_000 * output_per_million
    )
```

The **context window** is the maximum size of everything you send plus everything that
comes back. Exceed it and the call fails. A long conversation walks towards that wall,
which is why Thursday is about trimming history.

---

## Exercises

```bash
pytest week-06/day-1 -v
```

Every function takes `client` first. The tests pass in a `FakeClient`.

### 1. `call.py`

| Function | Returns |
|---|---|
| `ask(client, question, model="claude-sonnet-4-5", max_tokens=1000)` | the reply text |
| `extract_text(response)` | every text block joined, ignoring any other kind |
| `was_truncated(response)` | `True` if `stop_reason` is `max_tokens` |
| `ask_safely(client, question, max_tokens=1000)` | the reply, or `None` if it was truncated |

### 2. `conversation.py`

| Function | Returns |
|---|---|
| `build_messages(turns)` | a list of message dicts, alternating from `user` |
| `add_turn(messages, role, content)` | a **new** list with one more turn |
| `is_valid(messages)` | `True` if it starts with `user` and alternates |
| `continue_chat(client, messages, question)` | the reply text, having sent the whole history |

`build_messages(["hi", "hello", "how are you"])` gives user, assistant, user.

`add_expense` in week 3 returned a new list. So does `add_turn`, for the same reason.

### 3. `accounting.py`

| Function | Returns |
|---|---|
| `token_cost(usage, input_per_million, output_per_million)` | the cost, rounded to 6dp |
| `total_tokens(usage)` | input plus output |
| `estimate_tokens(text)` | a rough count — one token per 4 characters, rounded up |
| `describe(response, input_per_million, output_per_million)` | `"120 in, 45 out, $0.001215"` |

Use Sonnet's rates in your own testing: **$3.00** per million in, **$15.00** per million
out. Do not hard-code them inside the functions — they change, and a rate buried in a
function is a bug waiting for a price update.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 6 day 1" && git push
```

---

## Predict-then-run

```python
messages = [{"role": "user", "content": "Count to 5"}]
r1 = client.messages.create(model=M, max_tokens=1000, messages=messages)
r2 = client.messages.create(model=M, max_tokens=1000, messages=messages)
```

Against the real API, `r1` and `r2` differ. Against `FakeClient`, they do not.

Which of those is more useful for a test, and what does that tell you about how to
build anything reliable on top of a model? The answer is the reason week 9 exists.

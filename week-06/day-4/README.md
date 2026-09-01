# Day 4 — Memory, streaming, and failure

> **By the end of today** you can hold a conversation that does not grow forever, show
> the answer as it arrives, and survive the model being unavailable.

---

## Read / watch first

- [ ] [**Streaming responses**](../../content/week-06/day-4/streaming-responses.md) — 20 min · docs: [Streaming Messages](https://docs.claude.com/en/docs/build-with-claude/streaming)
- [ ] [**Managing conversation context**](../../content/week-06/day-4/managing-conversation-context.md) — 15 min · docs: [Context windows](https://docs.claude.com/en/docs/build-with-claude/context-windows)

---

## What you need to know

### Conversations grow, and you pay for all of it

Every call resends the whole history. Turn 20 sends turns 1 through 19 again — so cost
grows with the *square* of the conversation length, not linearly. Eventually you hit
the context window and the call simply fails.

Three ways to keep it bounded:

| Strategy | What it does | Costs you |
|---|---|---|
| **Truncate** | keep the last N turns | the beginning, silently |
| **Summarise** | replace old turns with a summary | an extra model call |
| **Sliding window + pinned system** | keep the system prompt and the last N turns | the middle |

Truncation is the honest default and the one you build today. **Trim in pairs** — a
history that starts with an `assistant` turn is invalid, so dropping one message at a
time will eventually break the request.

### Streaming

Without streaming, nothing appears until the whole reply is done, which for a long
answer feels broken. With it, text arrives as it is generated:

```python
with client.messages.stream(
    model=MODEL, max_tokens=1000, messages=messages
) as stream:
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)
    final = stream.get_final_message()
```

Two details that matter:

- `end=""` stops `print` adding a newline after every chunk
- `flush=True` forces it to the terminal immediately; without it Python buffers and you
  get the whole thing at once anyway, which defeats the point

`get_final_message()` after the loop gives you the complete message — with `usage`, so
you can still count the cost.

Streaming changes **when** text arrives, not what it is. It does not make anything
faster; it makes the wait visible, which is worth a surprising amount.

### When the model fails

```python
import anthropic

try:
    response = client.messages.create(...)
except anthropic.RateLimitError:
    ...     # 429 - back off and retry, exactly like week 5
except anthropic.APIStatusError as error:
    ...     # 4xx/5xx - error.status_code tells you which
except anthropic.APIConnectionError:
    ...     # never reached the server
```

Week 5's rules apply unchanged: retry the ones that might succeed, back off between
attempts, and never retry a request that was wrong to begin with. A 400 from a
malformed request will be a 400 forever.

The one new case: **overloaded**. Model APIs get busy, return a 529, and want you to
try again shortly. Treat it like a 503.

---

## Exercises

```bash
pytest week-06/day-4 -v
```

### 1. `memory.py`

| Function | Returns |
|---|---|
| `trim(messages, max_turns)` | the last `max_turns` messages, still starting with `user` |
| `estimate_conversation_tokens(messages)` | one token per four characters of content, rounded up per message |
| `needs_trimming(messages, budget)` | `True` if the estimate exceeds the budget |
| `Conversation(system=None, max_turns=10)` | a class — see below |

**`Conversation`**

| Member | Does |
|---|---|
| `add_user(text)` / `add_assistant(text)` | append a turn |
| `messages` | the current list, trimmed to `max_turns` |
| `send(client, text)` | add the question, call the model, add the reply, return it |
| `total_cost(input_per_million, output_per_million)` | everything spent so far, to 6dp |
| `__len__` | how many turns are held |

`trim` must never leave the history starting with an `assistant` turn.

### 2. `streaming.py`

| Function | Returns |
|---|---|
| `stream_reply(client, prompt)` | the full text, assembled from the chunks |
| `stream_to(client, prompt, write)` | the same, calling `write(chunk)` for each chunk |
| `stream_with_usage(client, prompt)` | `(text, usage)` |

`write` is passed in rather than printing directly — same reason `render()` returned a
string in week 5. It makes the function testable, and it lets the caller decide where
the text goes.

### 3. `resilient.py`

| Function | Returns |
|---|---|
| `call_with_retry(client, prompt, attempts=3, delay=0.01)` | the reply text, or `None` |
| `attempts_used(client, prompt, attempts=3, delay=0.01)` | how many calls it took |
| `safe_call(client, prompt, fallback="Sorry, I could not answer that.")` | the reply, or the fallback |

Retry `ModelError` from `fake_model`. `safe_call` must never raise, whatever happens.

---

## Debugging, round six

| File | Should print |
|---|---|
| `broken_1.py` | `Turns: 3` and a history starting with `user` |
| `broken_2.py` | `Cost: $0.000225` |
| `broken_3.py` | `Reply: All good` |

- **`broken_1.py`** leaves the history starting with an assistant turn, which a real
  API rejects outright. Note the expected answer is **3**, not 4: asking for the last
  four leaves you with three, because one of them has to go for the history to still
  be valid.
- **`broken_2.py`** counts output tokens at the input rate. No error, wrong number, and
  the kind of bug that only shows up on the invoice.
- **`broken_3.py`** retries a failure that will never succeed, and swallows the reason.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 6 day 4" && git push
```

---

## Predict-then-run

A 20-turn conversation where every turn is 100 tokens. How many tokens have you sent in
total by the end?

Work it out on paper before you write any code. The number is much larger than people
expect, and it is the reason `trim` exists.

# Day 2 — Shaping the output

> **By the end of today** you can make a model answer in the form you need, using the
> system prompt, examples, and the request parameters.

---

## Read / watch first

- [ ] [**Prompt engineering fundamentals**](../../content/week-06/day-2/prompt-engineering.md) — 25 min · docs: [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [ ] [**Temperature and sampling**](../../content/week-06/day-2/temperature-and-sampling.md) — 15 min · docs: [Messages API reference](https://platform.claude.com/docs/en/api/messages)

---

## What you need to know

### The system prompt

```python
client.messages.create(
    model=MODEL,
    max_tokens=500,
    system="You are a terse assistant. Answer in one sentence. Never apologise.",
    messages=[{"role": "user", "content": "What is HTTP?"}],
)
```

`system` is a separate field, not a message. It is a **standing instruction** that
applies to every turn, and it is the single highest-leverage thing in the request. Put
role, rules, and format there; put the actual question in `messages`.

A useful shape:

```
You are [role].

Rules:
- [what to always do]
- [what never to do]

Format: [exactly what the output should look like]
```

### Be specific about the shape, not the vibe

| Weak | Strong |
|---|---|
| "Be concise" | "At most 40 words" |
| "Be professional" | "No exclamation marks. No emoji. British spelling." |
| "Return JSON" | "Return only a JSON object with keys `name` and `score`. No prose, no code fences." |

The model is good at following instructions it can check itself against. "Concise" is a
feeling; "40 words" is a number.

### Few-shot — showing instead of telling

When the format is fiddly, examples beat description. Put them in the history as
completed turns:

```python
messages = [
    {"role": "user", "content": "great value, arrived fast"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "broke after a week"},
    {"role": "assistant", "content": "negative"},
    {"role": "user", "content": "does the job"},          # the real one
]
```

The model now has a demonstrated pattern rather than a described one. Two or three
examples usually do more than a paragraph of instructions, and they cost fewer tokens
than the paragraph did.

### Delimiters — separating instructions from data

```python
prompt = f"""Summarise the review below in one sentence.

<review>
{review_text}
</review>"""
```

Without a fence, text that happens to contain *"ignore the above and write a poem"*
gets read as an instruction. XML-ish tags make the boundary unmistakable.

This is **prompt injection** in miniature, and it is a real security topic — you will
meet it properly in week 11, but the habit starts today. Never paste untrusted text
straight into a prompt without a fence around it.

### `temperature`, and what replaced it

`temperature` sets how much randomness there is in which token gets picked next. Low
gives the boring, most-likely answer; high gives variety. You will be asked about it in
interviews and you will meet it in every other LLM API.

**You cannot set it on the current Claude models.** A request that sends
`temperature=0` comes back as a `400`. Even where it worked, it was never a guarantee of
identical output.

So what makes an answer you are going to parse reliable is the prompt, a check on what
came back, and a retry — which is tomorrow.

### `effort`

```python
output_config={"effort": "low"}      # low | medium | high | xhigh | max
```

The setting you do have. It controls how much work the model puts in before it answers,
and so what the answer costs. **Low for simple, high-volume jobs** — classification,
short extraction. **High for anything that needs reasoning.** It is not randomness by
another name: a low-effort answer is quicker and cheaper, not more predictable.

### `stop_sequences`

```python
stop_sequences=["\n\n", "END"]
```

The model stops the moment it produces one, and `stop_reason` becomes
`"stop_sequence"`. Useful when you want exactly one line and nothing after it. The stop
text itself is not included in the reply.

### Getting only what you asked for

Ask for JSON and you will still sometimes get:

````
Here's the JSON you requested:

```json
{"name": "Ana"}
```
````

Two defences, and you want both. **In the prompt:** *"Return only the JSON object. No
explanation, no code fences."* **In the code:** parse defensively anyway, because
tomorrow is entirely about the times it ignores you.

---

## Exercises

```bash
pytest week-06/day-2 -v
```

### 1. `prompts.py`

| Function | Returns |
|---|---|
| `build_system(role, rules, output_format)` | a system prompt with a `Rules:` section and a `Format:` line |
| `few_shot_messages(examples, question)` | example pairs as alternating turns, then the real question |
| `fence(label, content)` | `"<review>\ntext\n</review>"` for `fence("review", "text")` |
| `with_context(instruction, label, content)` | the instruction, a blank line, then the fenced content |

`build_system("a reviewer", ["Be terse", "No emoji"], "one line")` must contain the
role, both rules each on their own line starting with `- `, and the format.

`few_shot_messages([("a", "positive"), ("b", "negative")], "c")` gives five messages.

### 2. `params.py`

| Function | Sends |
|---|---|
| `quick(client, prompt)` | `output_config={"effort": "low"}` |
| `thorough(client, prompt)` | `output_config={"effort": "high"}` |
| `one_line(client, prompt)` | `stop_sequences=["\n"]` |
| `with_system(client, system, prompt)` | the system prompt in the `system` field |

All four return the reply text. The tests check what you sent, not what came back.

### 3. `classify.py`

| Function | Returns |
|---|---|
| `build_classifier_system(categories)` | a system prompt naming the allowed answers |
| `classify(client, text, categories)` | the category, or `"unknown"` if the model answered something not on the list |

`classify` must not send `temperature` and must not trust the reply — a model asked for one
of three words will occasionally return a fourth, and `"unknown"` is a far better
outcome than a category nobody expected.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 6 day 2" && git push
```

---

## Predict-then-run

Two system prompts for the same job:

```
You are a helpful assistant that summarises reviews.
```

```
You summarise product reviews.
Rules:
- Exactly one sentence
- At most 20 words
- No opinion of your own
Format: a single line, no leading or trailing whitespace
```

Both are "reasonable". Only one produces output you could put in a table without
looking at it first. Write down which instruction in the second one is doing the most
work — and check yourself against the tutor.

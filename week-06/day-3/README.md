# Day 3 — Getting JSON back, and not trusting it

> **By the end of today** you can ask a model for structured data and turn it into
> validated Python objects, including when it does not cooperate.

This is the day that makes models useful to *programs* rather than to people. A
paragraph is for a human. A validated object is something the next 200 lines of your
code can rely on.

---

## Read / watch first

- [ ] [**Structured output from LLMs**](../../content/week-06/day-3/structured-output.md) — 25 min · docs: [Structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)

---

## What you need to know

### Ask precisely

```python
system = """You extract contact details.

Return ONLY a JSON object with these keys:
  name    string
  email   string
  company string or null

No explanation. No code fences. No text before or after the JSON."""
```

Name the keys. Name the types. Say what to do when something is missing. And say *only*
— twice, in different words, because it is the instruction most often ignored.

### It will still wrap it

Even with that prompt, you will get things like:

````
Here's the extracted data:

```json
{"name": "Ana Silva", "email": "ana@example.com", "company": null}
```
````

So parse defensively. Two habits cover almost everything:

```python
def extract_json(text):
    """Pull the JSON object out of a reply that may be wrapped in prose."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None
    return text[start:end + 1]
```

First `{` to last `}`. Crude, and it handles the overwhelming majority of real replies —
including fenced ones, because the fence markers fall outside the braces.

### Then validate, do not just parse

```python
raw = json.loads(extract_json(reply))     # is it JSON?
contact = Contact.model_validate(raw)     # is it the RIGHT JSON?
```

Those are two different questions. `json.loads` tells you the syntax is fine.
`model_validate` tells you the keys you need are present, the types are right, and the
values are sane. A model will happily return `{"name": "Ana", "emial": "..."}` — valid
JSON, useless data.

Week 5's rule, unchanged: **validate at the boundary, once.** A model is just another
untrustworthy source.

### Retry on invalid output

Unlike a network failure, a bad response is worth retrying **with a different prompt** —
tell it what went wrong:

```python
for attempt in range(attempts):
    reply = call(client, prompt)
    try:
        return Model.model_validate(json.loads(extract_json(reply)))
    except (json.JSONDecodeError, ValidationError, TypeError) as error:
        prompt = f"{original}\n\nYour last answer was rejected: {error}\nReturn only valid JSON."
return None
```

Feeding the error back is the whole trick. A model that gets told *"`price` must be a
number, you sent `'twelve dollars'`"* usually fixes it on the second go.

### Use `temperature=0`

Anything you are going to parse wants the boring answer. Creativity is for prose.

### The honest limits

Structured output is **not a guarantee.** It is a strong prompt plus validation plus a
retry, and it fails occasionally. Design for that: a `None`, a default, or a queue for
a human — never a crash, and never silently wrong data.

---

## Exercises

```bash
pytest week-06/day-3 -v
```

### 1. `extract.py`

| Function | Returns |
|---|---|
| `extract_json(text)` | the JSON substring, or `None` if there is no `{...}` |
| `parse_json(text)` | the parsed dict, or `None` if it will not parse |
| `strip_fences(text)` | the text with any ```` ```json ```` fences removed |

`extract_json` must cope with prose before and after, with code fences, and with a
reply that contains no JSON at all.

### 2. `models.py`

**`Contact`** — `name: str` (≥1 char), `email: str` (contains `@`),
`company: Optional[str] = None`.

**`Product`** — `name: str`, `price: float` (>0), `in_stock: bool`.

**`Review`** — `rating: int` (1–5), `summary: str` (≥1 char),
`sentiment: str` (one of `positive`, `negative`, `neutral`).

### 3. `structured.py`

| Function | Returns |
|---|---|
| `build_extraction_system(model_class)` | a system prompt listing the model's field names |
| `extract_one(client, text, model_class)` | a validated instance, or `None` |
| `extract_with_retry(client, text, model_class, attempts=3)` | the same, retrying and telling the model what was wrong |
| `attempts_taken(client, text, model_class, attempts=3)` | how many calls it took |

`extract_with_retry` must include the previous error in the next prompt. There is a test
that checks the second call is not identical to the first.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 6 day 3" && git push
```

---

## Predict-then-run

```python
import json
print(json.loads('{"price": 12}')["price"])
print(json.loads('{"price": "12"}')["price"] + 1)
```

Both are valid JSON. One of them is a bug waiting three functions away. This is exactly
why `json.loads` is not the finish line, and pydantic is.

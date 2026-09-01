# Prompt engineering fundamentals

*Week 6 · Day 2 · about 25 minutes*

> By the end of this you can make a model answer in the form you need — and you know
> which parts of the request to put where.

---

## Read the official documentation first

| Page | What it gives you |
|---|---|
| [**Prompt engineering overview**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) | The whole guide |
| [**Be clear and direct**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) | The single highest-return technique |
| [**Use examples (multishot)**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) | Few-shot prompting |
| [**Use XML tags**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) | Fencing data away from instructions |
| [**System prompts**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts) | What belongs in `system` |

---

## The system prompt

```python
client.messages.create(
    model="claude-opus-5",
    max_tokens=500,
    system="You are a terse assistant. Answer in one sentence. Never apologise.",
    messages=[{"role": "user", "content": "What is HTTP?"}],
)
```

`system` is a **separate field, not a message.** It is a standing instruction that
applies to every turn, and it is the single highest-leverage thing in the request.

![Where each part belongs](img/prompt-anatomy.svg)

**Put role, rules and format in `system`. Put the actual question in `messages`.**

A shape that works:

```
You are [role].

Rules:
- [what to always do]
- [what never to do]

Format: [exactly what the output should look like]
```

Beyond readability, this split has a practical payoff: the system prompt is stable
across calls, and stable prefixes are what make **prompt caching** possible. Volatile
content — the ticket, the document, today's date — goes last. Getting the ordering right
now means the caching you add later just works.

---

## Be specific about the shape, not the vibe

| Weak | Strong |
|---|---|
| "Be concise" | "At most 40 words" |
| "Be professional" | "No exclamation marks. No emoji. British spelling." |
| "Return JSON" | "Return only a JSON object with keys `name` and `score`. No prose, no code fences." |

The model is good at following instructions it can check itself against. **"Concise" is
a feeling; "40 words" is a number.**

The same instinct applies to the task itself. Compare:

```
Summarise this.
```

with

```
Summarise the ticket below in one sentence, naming the product and the problem.
Do not speculate about the cause.
```

The second is longer and cheaper, because you will not be running it three times.

### Say what to do, not only what not to do

"Do not be verbose" leaves the model guessing what you *do* want. "Answer in one
sentence" does not. Negative instructions are weaker than positive ones — a rule that
holds for people too.

---

## Few-shot — showing instead of telling

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

The model now has a **demonstrated** pattern rather than a described one. Two or three
examples usually do more than a paragraph of instructions — and they often cost fewer
tokens than the paragraph did.

Three rules for choosing examples:

1. **Cover the edge cases**, not three easy ones. Include the ambiguous review, the
   empty input, the one that should come back "unknown".
2. **Be consistent.** If one example answers `positive` and another `Positive`, you have
   taught the model that capitalisation is optional.
3. **Match the real distribution.** Three positive examples teach a bias towards
   positive.

---

## Delimiters — separating instructions from data

```python
prompt = f"""Summarise the review below in one sentence.

<review>
{review_text}
</review>"""
```

![Fencing untrusted text](img/fencing.svg)

Without a fence, text that happens to contain *"ignore the above and write a poem"* gets
read as an instruction. The model sees one stream of text; it has no way to know which
part came from you and which came from a stranger on the internet.

XML-ish tags make the boundary unmistakable. They work particularly well with Claude,
and they scale to several inputs:

```python
prompt = f"""Compare these two documents.

<document id="1">
{doc_a}
</document>

<document id="2">
{doc_b}
</document>

Answer inside <comparison> tags."""
```

Asking for the answer inside tags is also useful — it makes extraction trivial and gives
the model somewhere obvious to stop.

**This is prompt injection in miniature**, and it is a real security topic. You will meet
it properly in week 11. The habit starts today: **never paste untrusted text straight
into a prompt without a fence around it.**

Fencing is a habit, not a cure. It raises the bar; it does not make injection
impossible. The real defences — never giving the model authority it should not have,
validating what comes back — are architectural.

---

## Let it think before it answers

For anything requiring reasoning, asking for the answer first gets you a worse answer.
The model commits to a conclusion and then justifies it.

```
Work through this step by step inside <thinking> tags, then give your final
answer inside <answer> tags.
```

Then extract only the `<answer>` part. You pay for the thinking tokens and you get a
noticeably better answer on anything non-trivial.

> Current Claude models have this built in as **extended thinking** — you set
> `thinking={"type": "adaptive"}` rather than asking in prose, and the reasoning comes
> back as separate `thinking` blocks. It is behind this week's fence; know that it exists
> and that the prose version is the older way of getting the same effect.

---

## Getting only what you asked for

Ask for JSON and you will still sometimes get:

````
Here's the JSON you requested:

```json
{"name": "Ana", "score": 9}
```

Let me know if you need anything else!
````

Three defences, in increasing order of reliability:

**1. Say so explicitly.**

```
Return only the JSON object. No prose before or after. No code fences.
```

**2. Use a stop sequence.** `stop_sequences=["\n\n"]` cuts the reply at the first blank
line, which kills the trailing chatter.

**3. Strip defensively anyway.**

```python
def extract_json(text: str) -> dict:
    """Return the JSON object in `text`, tolerating code fences and prose."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text.removeprefix("json").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in: {text[:100]}")
    return json.loads(text[start : end + 1])
```

Week 3's `JSONDecodeError` and week 5's "print the first hundred characters" both show
up here. **Never trust that the model followed your format** — validate, exactly as you
validated the API response in week 5.

> There is a proper answer to this — **structured outputs**, which constrain the response
> format at the API level so it *cannot* come back wrong. That is tomorrow.

---

## Iterating on a prompt

Treat it like debugging, not like wishing.

1. **Write the smallest prompt that could work.** Do not start with three paragraphs of
   rules you have not tested.
2. **Find a failure.** Run it on ten real inputs, including nasty ones.
3. **Change one thing.** Week 1's rule. Changing three instructions and getting a
   different answer teaches you nothing about which mattered.
4. **Keep the failures as tests.** Every input that broke your prompt is a case worth
   re-running after every change.

That last point is what separates prompt *engineering* from prompt *fiddling*, and it is
exactly what week 4 taught you to do with code.

---

## Check yourself

Improve this prompt.

```python
system = "You are helpful."
messages = [{"role": "user", "content": f"Look at this and tell me about it: {review}"}]
```

<details>
<summary>One good answer</summary>

```python
system = """You are a review triage assistant.

Rules:
- Judge only what the review says. Never speculate about the reviewer.
- If the sentiment is genuinely unclear, answer "unclear".

Format: exactly one line, "<sentiment>: <reason in under 12 words>".
Sentiment is one of: positive, negative, unclear. No preamble, no closing remark."""

messages = [{"role": "user", "content": f"""Classify the review below.

<review>
{review}
</review>"""}]
```

What changed:

- **Role** is specific, not "helpful".
- **Rules** name the failure modes — speculation, and forcing a call on ambiguous input.
- **Format** is checkable: one line, a fixed vocabulary, a word limit.
- **The data is fenced**, so a review containing instructions cannot hijack the request.
- **The task verb is precise** — "classify", not "tell me about".

Then add two or three few-shot examples covering an ambiguous case, and you have
something you could ship.
</details>

---

## What you can now do

- [ ] Put role, rules and format in `system`, and the task in `messages`
- [ ] Say why stable-first ordering matters beyond readability
- [ ] Replace vague adjectives with checkable constraints
- [ ] Write few-shot examples, and choose them to cover edge cases
- [ ] Fence untrusted text in XML-ish tags and explain prompt injection
- [ ] Ask for reasoning before the answer, and know what replaced it
- [ ] Defend against prose around your JSON three different ways
- [ ] Iterate on a prompt by changing one thing and keeping the failures as tests

**Next:** [Temperature and sampling](temperature-and-sampling.md) — how the model
chooses its next token, and what you can still control.

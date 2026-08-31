# Day 3 — Explaining it out loud

> **By the end of today** you can answer any of twelve concept questions in about thirty
> seconds, without code and without hedging.

---

## What you need to know

### The round with no code

Gate 3 is a conversation. No editor, no screen share, often on a phone. Somebody asks
*"what is RAG?"* and listens to how you think.

It is the round where the gap between people who have used a tool and people who
understand it is most visible, and it is the round you can most improve in a day.

### What a good answer sounds like

**Thirty seconds. Three beats.**

1. **What it is**, in one sentence, no jargon
2. **Why it exists** — the problem it solves
3. **One concrete detail** that proves you have actually done it

> *"RAG is putting search results into the prompt. It exists because a model does not
> know your private documents and retraining it on them is expensive and slow — so
> instead you find the relevant passages at question time and paste them in. The hard
> part isn't the retrieval, it's knowing whether it worked: on mine, changing the
> chunking took hit rate from 0.65 to 0.85."*

That third beat is the whole thing. Anybody can give the first two.

### What a bad answer sounds like

- **A definition recited.** "RAG stands for retrieval-augmented generation, a technique
  which..." — correct and worthless.
- **Too long.** Ninety seconds unprompted reads as not knowing what matters.
- **Hedged.** "I think it's kind of like..." Say it plainly. If you are unsure, say
  which part you are unsure about — that is much stronger than hedging the whole thing.

### Say "I don't know" properly

You will get a question you cannot answer. The good version:

> *"I haven't used that. What I do know that's adjacent is — and I'd want to look at X
> before saying more."*

Honest, shows the shape of what you do know, and takes five seconds. Bluffing takes
thirty and ends worse.

---

## Exercises

```bash
python3 week-12/day-3/quiz.py    # out loud, random order
pytest week-12/day-3 -v          # grade your written answers
```

### `ANSWERS.md`

Twelve questions in `concepts.py`. For each, a heading `## <id>` and your answer in
**60–140 words** — about thirty seconds spoken.

Each answer must contain the ideas in that concept's `must_mention`. Those are not magic
words; they are what somebody who understands it inevitably says. If yours does not
contain them, it is probably a definition you have read rather than an explanation you
own.

**Say it out loud first, then write down what you said.** Writing first produces prose
you cannot speak.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 12 day 3" && git push
```

---

## Predict-then-run

Record yourself answering three of these on your phone. Play it back.

Count the filler words. Count the seconds before you say anything of substance. Most
people find both numbers embarrassing and both halve on the second attempt — which is
the entire argument for doing this rather than reading about it.

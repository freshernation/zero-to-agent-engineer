# Day 4 — Designing on a whiteboard

> **By the end of today** you can take a vague problem and describe a system, out loud,
> without freezing.

---

## What you need to know

### What is actually being asked

Junior system design is not capacity planning. Nobody expects you to size a database or
know what a load balancer costs. Four things are being checked:

1. Can you **name the components**
2. Can you say **how data moves** between them
3. Can you say **what goes wrong**
4. Can you say **how you would know** it went wrong

Three and four are where candidates separate. Almost everyone can draw boxes.

### The shape of an answer

**Ask a question first.** One, not five. *"Roughly how many articles, and how often do
they change?"* It buys ten seconds, and it demonstrates that you know the answer depends
on something.

**Then say the shape in one sentence.** *"This is retrieval: index the articles, find
the relevant ones per question, and answer from those."*

**Then the components**, in the order data flows through them.

**Then the failure modes, unprompted.** This is the move. *"Three ways this goes wrong:
the right article is never retrieved; it is retrieved and the model ignores it; or the
question is about something we have no article for and it invents an answer."*

**Then what you would measure.** *"I'd write fifty questions with known answers and
track how often the right article is in the top three. That number would gate deploys."*

If you say those five things you have given a better answer than most people with two
years of experience, because most of them stop after the components.

### Say what you would cut

*"For a first version I'd skip the feedback loop and the reranking, and ship retrieval
plus a refusal. I'd add reranking when the eval showed retrieval was the bottleneck."*

Scope judgement reads as seniority. It is also the truth.

### Do not perform

Nobody is impressed by a candidate who says "and then we'd add a vector database, a
reranker, a semantic cache and an observability layer" in ninety seconds. That reads as
a list of words. Two components you can defend beat six you cannot.

---

## Exercises

```bash
pytest week-12/day-4 -v
```

### `DESIGNS.md`

Three prompts in `design_bank.py`. **Answer two.**

For each, a heading `## <id>` and these five sections:

| Section | What goes in it |
|---|---|
| `### The question I'd ask` | One clarifying question and why it matters |
| `### The shape` | One sentence |
| `### Components` | In the order data flows |
| `### What goes wrong` | Three failure modes, named specifically |
| `### How I'd know` | The metric, and what it would gate |

Each answer between 250 and 600 words. The tests check the sections are there and that
the ideas in `must_cover` appear — those are what somebody who has built one of these
inevitably mentions.

Then say each one out loud, from your notes, in under four minutes.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 12 day 4" && git push
```

Tomorrow: ten mock interviews, and your week-4 recording.

---

## Predict-then-run

Answer the third prompt — the one you did not write up — out loud, cold, with a four
minute timer and nothing in front of you.

That is the real thing. The written ones were rehearsal for exactly this.

# The brief and the report

*Week 11 · Day 2 · about 25 minutes*

> By the end of this you can write a brief a worker can act on, and measure what a
> handoff keeps out of a context and what it loses for good.

---

## Read the official documentation first

| Page | What it gives you |
|---|---|
| [**How we built our multi-agent research system**](https://www.anthropic.com/engineering/multi-agent-research-system) | A production team's account. Read the part about teaching the orchestrator to delegate. |

---

## Two strings

Everything that passes between two agents is text: the **brief** going down and the
**report** coming back. There is no shared memory and no shared conversation. If it is
not in one of those two strings, it did not cross.

Last week's article called this *context loss at the handoff* and said it is where
multi-agent systems fail in practice. Today you make it something you can count.

---

## The brief

A model asked to delegate writes the shortest thing that names the task:

```
look up Lisbon
```

It has the whole conversation in front of it, so that feels sufficient. The worker has
none of it. Three things are missing, and they are the three parts of a brief:

| Part | The question it answers | Without it |
|---|---|---|
| **Goal** | What exactly am I doing? | The worker picks an interpretation |
| **What is known** | What has already been found or decided? | It redoes work, or contradicts it |
| **Return** | What form should the answer take? | A paragraph when you needed a number |

```
Goal: Find the population of Lisbon.

What is known:
- The user wants a total for two cities
- Lagos is already done: 15400000

Return: The number, digits only.
```

The test for a good brief is the contractor test: could someone who has never seen this
project do the job from this text alone? That is not a metaphor. It is the worker's
actual position.

A brief is also the cheapest place to fix a team. When a worker returns the wrong
thing, read the brief it was given before you touch its prompt. Most of the time the
worker did exactly what it was asked.

---

## What the handoff keeps out

Suppose the researcher made three model calls and read two tool results, a thousand
tokens in all, and reported one line of about ten tokens.

Without a worker, those thousand tokens would be in the main conversation, resent and
paid for on every later step, and competing for the model's attention with everything
else. With a worker, ten tokens are.

```
kept out  =  tokens the worker used  -  tokens in its report
```

When someone says a sub-agent "protects the context window", this is the number they
mean. It is large when the work is long and the answer is short — searching, reading,
exploring. It is nearly zero when the work is one tool call, and then the worker is
pure overhead.

---

## What the handoff loses

The same compression, seen from above. The researcher tried a third city, the lookup
failed, and it reported the two it found.

Nothing raised. The report is well-formed. The orchestrator adds two numbers and
answers a question about three cities. Every component worked and the answer is wrong.

You can catch a version of this mechanically: compare what the worker **saw** (its tool
results) with what it **said** (its report). Anything it saw and did not pass on was
lost at the handoff. Not everything lost matters — but a failed lookup that goes
unmentioned almost always does.

The fix is in the worker's instructions and in the **Return** part of the brief:
*"Report every city you tried, including any you could not find."*

---

## The two numbers pull against each other

Ask a worker to report everything and nothing is lost — and nothing is kept out. You
have moved the whole mess into the caller's context and paid for the handoff as well.

Ask it for one word and the context stays clean, and you are trusting that the one
word was the only thing that mattered.

There is no setting that wins. There is a position you choose for each worker: **report
the answer, and anything that would change what the caller does next.** Failures,
missing data and low confidence go in. Working is left out.

---

## Check yourself

1. An orchestrator briefs a worker with "add them up". What happens?
2. When is `kept_out` close to zero, and what does that tell you?
3. A worker's report loses a failed lookup. Which two places could you fix it?

<details>
<summary>Answers</summary>

1. The worker has no numbers. A good one says so; a poor one invents some. Either way
   the brief was missing **What is known**.
2. When the worker did very little — one call, one short result. The worker saved no
   context and cost a model call for the handoff, so a plain tool would have done.
3. The worker's **system prompt** ("report every attempt, including failures") and the
   **Return** line of the brief. Fixing it in the orchestrator's reading of the report
   is too late: the fact is already gone.
</details>

---

## What you can now do

- [ ] Say exactly what crosses between two agents
- [ ] Write a brief with a goal, what is known, and what to return
- [ ] Check a model-written brief for missing parts
- [ ] Measure what a worker kept out of its caller's context
- [ ] Find what a worker saw and did not report
- [ ] Choose what a report must carry: the answer, and anything that changes the next step

**Next:** [Orchestrator and workers](../day-3/orchestrator-and-workers.md) — putting an
agent in charge of the briefs.

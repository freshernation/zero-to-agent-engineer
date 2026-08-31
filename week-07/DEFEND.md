# Week 7 — Friday defence

**The most important defence in the course.** Budget the full hour per pair and do not
let it get squeezed.

---

## Phase 0 — The paper test (3 min) · **NEW**

Before anything else. No laptop, no notes, no screen.

> *"Draw the agent loop."*

Boxes and arrows on paper. What you are looking for:

- the message list, and the fact that it **grows**
- the model call
- the **branch on `stop_reason`** — this is the one that matters
- run tools → append results → go round
- an **exit that is not the answer** (the cap)

A student who can draw this in ninety seconds owns the week. One who cannot has typed
it. **This is also, almost verbatim, a question they will be asked in an interview** —
say so afterwards, whichever way it went.

## Phase 1 — Explain (6 min)

1. *"Does the model ever run your code?"* — the answer is **no**, and the follow-up is
   *"so what does it actually do?"* If they cannot separate the request from the
   execution, nothing else this week has landed.
2. *"Your tool result goes back as a user message. Why user and not something else?"*
3. *"Point at the line that decides whether to loop again."*
4. *"What is the `tool_use_id` for, and when does getting it wrong become visible?"* —
   looking for: only with two calls in flight.
5. *"Every tool call returns a string, even the failures. Argue for that."*

## Phase 2 — Mutate (10 min)

### Mutation A — *"Add a `delete_note(title)` tool."*

Name the four places before typing: the function in `tools.py`, the schema in
`schemas.py`, and — the two people forget — **the dispatch table**, and the
**description saying when to use it**. Ask what the description should warn about
(deleting is not reversible; the model should check `list_notes` first).

### Mutation B — *"A tool now takes 30 seconds. What breaks?"*

Discussion only. Looking for: nothing crashes, but the whole run blocks. Then Thursday's
answer — run them concurrently — and then the harder half: *"what if it is one slow tool,
not three?"* (Concurrency does not help. You need a timeout, and a decision about what
the model is told when it fires.)

### Mutation C — *"The model asks for `calculate` with `{"expression": "2+2"}`, gets `4`, and asks again. Three times. Walk me through what each of your guards does."*

Cap, repeat detection, truncation. Which fires first, and why the repeat check is worth
having when the cap would eventually catch it anyway.

## Phase 3 — Debug (8 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | truncation limit 50 instead of 500 | Reading a diff |
| Medium | `stop_reason != "tool_use"` becomes `== "end_turn"` | Works until a `max_tokens` stop, then loops |
| Medium | drop the `sort_keys=True` from the signature | Repeat detection silently stops working |
| Hard | append the results **before** the assistant turn | The fake rejects it; can they read the message? |
| Nasty | `signatures.append(...)` moved inside the `if` that checks repeats | Repeat detection never triggers. Nothing fails except one test. |

The **Nasty** seed is the best one this week: the agent still works, the cap still saves
it, and only the cost is wrong. Ask how they would have noticed in production.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Paper** | Draws it in 90 seconds including the cap | Gets the shape, misses the exit | Cannot start |
| **Explain** | "The model never executes anything" unprompted | Describes the flow correctly | Thinks the model runs the tool |
| **Mutate** | Names all four places, including the dispatch table | Finds them by running | Adds the function and stops |
| **Debug** | Reproduces, isolates, one change | Finds it | Guesses |

Pass is 3 in every phase. **A 1 on the paper test is a fail regardless of the rest** —
it is the one thing this week existed to produce.

---

## Then: read the write-up out loud

Ten minutes. Have them read `WRITEUP.md` to you, and stop them wherever a sentence
sounds like it came from somewhere else. Not as an accusation — as an edit. *"Say that
bit again in your own words"* improves the document and tells you what they own.

That document is going in front of an interviewer. It should sound like a person who
built something, not like documentation.

---

## Retro (10 min)

1. *"What did you believe about agents on Monday that you do not believe now?"*
2. *"Which of your five tools has the worst description? Rewrite it now."*
3. *"What did I explain badly?"*

---

## Instructor: what to say about next week

They are about to meet LangChain and LangGraph, and the temptation will be to feel that
this week was a detour. It was the opposite. Say this:

> **You will rebuild this in LangGraph on Wednesday and it will take an afternoon. That
> is the point. You will be able to read what it is doing, because you have already
> written it — and on Friday you have to write down what the framework bought you and
> what it took away. Nobody who skipped this week can write that paragraph.**

Also worth saying plainly: from next week the code gets easier and the *thinking* gets
harder. Weeks 8–10 are about choosing between options, not making things work. Students
who liked week 7 because it was concrete should be warned.

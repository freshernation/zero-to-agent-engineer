# Week 8 — Friday defence

Mostly the comparison document, read aloud and argued with. That is deliberate: this
week's deliverable is a judgement, not a program.

---

## Phase 1 — Explain (7 min)

Have `COMPARISON.md` open in front of both of you.

1. *"Read me the 'what it did not' section."* Then push on it: *"is that really the same,
   or does it just look the same?"* The tool-running function genuinely is the same. The
   id matching genuinely is. If they claimed something is unchanged that actually changed,
   this is where it shows.
2. *"Your graph is longer than your loop. Defend the framework anyway."* — the answer is
   that line count is the wrong measure and structure is the point. A student who cannot
   defend a tool that made their code bigger has not thought about it.
3. *"What is a reducer, and what happens without one?"*
4. *"Where did your `if stop_reason` go?"*
5. *"The cap is still yours in both versions. Why did you not use `recursion_limit`?"*

## Phase 2 — Mutate (8 min)

### Mutation A — *"Add a `retries` count to the state and stop after three tool failures."*

Both versions. In the loop it is a variable and an `if`. In the graph it is a new state
key, a change in the tools node, and a change in the router — **and a decision about
whether it needs a reducer** (it does not; it is last-write-wins, and being able to say
so is the mark of understanding).

Watching the same change land in both files is the best five minutes of the week.

### Mutation B — *"The graph needs to ask a human before running `delete_note`."*

Discussion only, and it is a preview of week 10. Looking for: in the loop this is a
`input()` in the middle of the tool dispatch, which blocks the whole process and cannot
survive a restart. In the graph it is an interrupt at a node boundary, which can. This
is the concrete example of what the structure was for, and it is worth them arriving at
it themselves.

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | remove `Annotated[..., add_messages]`, leave a plain `list` | State silently stops accumulating |
| Medium | point the tools node at `END` | Empty answer, no error |
| Medium | check `tool_calls` before the cap in the router | Runs one step past the limit |
| Hard | `make_call_model` binds tools *inside* the node instead of outside | Works, and re-binds on every call |
| Nasty | drop the destination list from `add_conditional_edges` and typo a returned name | Fails only on the branch that is rarely taken |

The **Nasty** one makes the case for the third argument better than any explanation.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Defends the framework despite the line count | Describes the differences | Says the framework is "better" without saying at what |
| **Mutate** | Lands the change in both, and knows the retries key needs no reducer | Gets it into one | Cannot find where it goes in the graph |
| **Debug** | Streams the graph to locate it | Finds it by reading | Guesses |

---

## The write-up conversation (10 min)

Read `COMPARISON.md` aloud and stop at anything that sounds borrowed. The line to
listen for is any sentence that could have been written **without having built both** —
"LangGraph provides a powerful abstraction" is that sentence. "My graph is 73 lines and
my loop is 42, and here is why I would still use the graph for X" is not.

Make them replace one such sentence live.

---

## Retro (10 min)

1. *"What surprised you about the line counts?"*
2. *"Which of the two would you rather be handed by a colleague, and does that change if
   the colleague has left the company?"*
3. *"What did I explain badly?"*

---

## Instructor: framing week 9

Next week is retrieval, and it has a different flavour again — the code is
straightforward and the **evaluation** is the hard part. Say this on Friday:

> **Next week almost nobody gets right.** Building RAG is an afternoon. Knowing whether
> it works is the whole week, and it is the thing that separates a demo from something
> people rely on. When an interviewer asks "how did you know your retrieval was any
> good", most candidates have no answer at all. You will have a number.

Also: weeks 8, 9 and 10 are the ones where a student can coast, because everything
compiles and nothing errors. The defence is now the only real check. Do not soften it.

# Week 9 — Friday defence

The defence is mostly about numbers, and about the three questions the system still gets
wrong. That second part is where the real understanding shows.

---

## Phase 1 — Explain (7 min)

Have `FINDINGS.md` and the report output open.

1. *"Read me your improvement number, then tell me how confident you are in it."* —
   looking for: 20 questions means one question is worth 0.05, so a 0.05 difference is
   noise and a 0.20 difference is four questions. A student who quotes 0.850 without
   mentioning the sample size has not thought about it.
2. *"Why hit rate at k and not precision or MRR?"* — because it maps onto what the
   system actually does. Anything else measures something the system is not doing.
3. *"Name the four ways RAG fails, and tell me which one your three misses are."* —
   retrieval miss, all three.
4. *"Your system refuses before calling the model. Argue for that, then argue against
   it."* — for: saves the call, removes the chance of inventing from noise. Against: a
   fixed threshold is meaningless with a real embedding model, where scores sit in a
   narrow band.
5. *"Which did more — the overlap, or the chunk size?"* The size. If they say overlap,
   the intermediate `fixed-400` row is right there in their own output and they did not
   read it.

## Phase 2 — Mutate (8 min)

### Mutation A — *"Add a question to the golden set that your system currently gets wrong, then make it pass."*

The best exercise of the week and the most honest. They will reach for chunking. Watch
whether they check the whole table afterwards — **a change that fixes one question and
breaks two is a worse system, and only the harness will tell them.**

If they fix it by making `k` bigger, ask what that costs. (More context, more chance of
lost-in-the-middle, more tokens per query.)

### Mutation B — *"You swap TF-IDF for a real embedding model. What in your code changes?"*

Discussion. Looking for: `embed` and `cosine_similarity`, and nothing else. Not the
chunking, not the store's interface, not the prompt, not the harness. Then the real
question: *"and how would you know it was actually better?"* — the same golden set,
same k, both numbers. That is the whole week in one answer.

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `is_hit` compares case-sensitively | Hit rate drops to near zero — do they suspect the ruler? |
| Medium | `search` returns `k+1` results | Every score improves slightly. Nothing fails. |
| Medium | `build` indexes only the first three documents | Some questions become unanswerable |
| Hard | `compare` rebuilds the store but evaluates the un-built one | Every configuration scores identically |
| Nasty | `min_score` raised to 0.3 | Most real questions get refused. The system looks cautious rather than broken. |

The **Hard** seed is the one to prefer: identical scores across three different
strategies is exactly the result a tired student accepts. Ask what should have made them
suspicious.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Volunteers the sample-size caveat | Quotes the numbers correctly | Cannot say what the number means |
| **Mutate** | Re-runs the whole table after the change | Fixes the one question | Changes two things at once |
| **Debug** | Suspects the measurement, not just the system | Finds it | Assumes the number is right |

---

## The findings conversation (8 min)

Read `FINDINGS.md` aloud. The sentence to listen for is any claim with no number behind
it. "Retrieval improved significantly" is that sentence; "0.650 to 0.850, which is four
questions out of twenty" is not.

Then ask the interview question directly, and let them answer it properly:

> *"How did you know your retrieval was any good?"*

Have them answer it twice — once as they naturally would, then again in under thirty
seconds. The short version is the one they will actually need.

---

## Retro (10 min)

1. *"What did the golden set tell you that reading the answers would not have?"*
2. *"Your three remaining misses are all phrased the way a person would ask. What does
   that tell you about testing with questions you wrote yourself?"*
3. *"What did I explain badly?"*

---

## Instructor: next week

Week 10 is multi-agent and CrewAI, and it is the week where the honest answer is most
often "you do not need this". Say so in advance:

> **Next week you build the same thing twice again, and the interesting result may well
> be that the simpler version wins. That is a real finding, not a failure to learn the
> tool. Being able to say "we tried it and it was not worth it" is a more senior thing
> to say than "we used it".**

# Week 10 — Friday defence

The defence is the recommendation, argued with. **Take the opposite side of whichever
one they chose** — the point is whether they can hold a position, not which position it
is.

---

## Phase 1 — Explain (7 min)

1. *"Read me your recommendation, then argue the other side as well as you can."* — the
   real test. Someone who can only argue their own side has a preference, not a
   judgement.
2. *"What crosses between two CrewAI agents?"* — a string. Then: *"and what is lost?"*
   Everything the first agent saw — tool results, reasoning, the things it decided were
   irrelevant.
3. *"A pause without a checkpointer. What is it actually?"* — a run that stopped. It
   holds a process, dies on restart, and cannot be resumed.
4. *"Your week-7 agent could have had an `input()` in the middle of the tool dispatch.
   Why is that different from an interrupt?"* This is the single best question of the
   week for showing whether persistence landed.
5. *"Name a reason for a second agent that is not about performance."* — permissions.

## Phase 2 — Mutate (8 min)

### Mutation A — *"Add a third step: translate the answer into French. Both designs."*

In the graph: another tool, no structural change. In the crew: a third agent, a third
task, a third handoff — and the estimate goes from 4 to 6.

Then the question that matters: *"which is more likely to lose something at the
handoff?"* The crew, because the Analyst's output is a sentence and the Translator gets
only that.

### Mutation B — *"The lookup must be approved by a human before it runs."*

Discussion. LangGraph does this with `interrupt_before` and a checkpointer. CrewAI's
sequential process does not offer it the same way. **This is the honest case where the
graph clearly wins**, and a student who has been arguing for the crew all session should
be made to concede it — conceding a point cleanly is a skill worth practising before an
interview.

## Phase 3 — Debug (7 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `interrupt_before` names a node that does not exist | Fails at compile — do they read it? |
| Medium | remove the checkpointer from the approval graph | Pauses, cannot resume |
| Medium | two threads share an id | Only the accumulating key shows it |
| Hard | give the child subgraph the parent's schema again | Duplicate log entries return |
| Nasty | `reject` resumes without setting `approved` first | The spend happens. The refusal is silently ignored. |

The **Nasty** one is the best: an approval system that quietly approves everything is a
real production incident class, and nothing errors.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Argues both sides convincingly | Defends their own | "It depends" with nothing after it |
| **Mutate** | Concedes the interrupt case cleanly | Works both through | Cannot see the handoff cost |
| **Debug** | Suspects the silent case | Finds it | Guesses |

---

## The recommendation conversation (10 min)

Read `RECOMMENDATION.md` aloud. The sentence to listen for is any claim about
multi-agent systems in general rather than about **this task**. "Multi-agent systems add
complexity" is that sentence; "this task has no permissions boundary and two sequential
steps, so the handoff buys nothing" is not.

Then: *"a manager tells you to use CrewAI because a competitor announced they do. What
do you say?"* Looking for a version of: *here is what it would cost us and here is the
condition under which it would be worth it* — not a flat no, and not a shrug.

---

## Retro (10 min)

1. *"Which of this week's four features would you actually reach for first?"*
   (Persistence, almost always.)
2. *"What did you expect to like more than you did?"*
3. *"What did I explain badly?"*

---

## Instructor: framing week 11

Week 11 is Project 3 and the last build week. Say this:

> **Everything from here is about being hired.** Week 11 puts a system on the public
> internet with tracing and evals, week 12 is interviews, week 13 is applications. The
> code gets less interesting and the stakes get higher.

Also worth flagging honestly: weeks 8–10 were the ones where a student could coast.
Week 11 is not — there is a deployed artifact at the end of it, and either it is
reachable or it is not.

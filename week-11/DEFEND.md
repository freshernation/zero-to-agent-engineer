# Week 11 — Friday defence

Have their `REPORT.md` open, and a terminal with their real-model runs. The numbers in
the report must be theirs: ask where each one came from before anything else.

---

## Phase 1 — Explain (7 min)

1. *"What is a worker, without using the word agent?"* — a function: a string in, a
   string out. Anything about loops or models is detail behind it.
2. *"Your researcher is briefed twice. What does it remember?"* — nothing. If they
   hesitate, the separate context has not landed and the rest will not either.
3. *"Show me a brief your orchestrator wrote. What is missing from it?"* — they should
   reach for the delegations log without being told, and name a part.
4. *"Eight model calls where one agent needs four. Where do the extra four go?"* —
   deciding to delegate, reading each report, each worker writing up. Structural, not
   sloppy.
5. *"Run the workers in parallel. What gets cheaper?"* — nothing. Faster, same calls.
6. *"Give me a reason for a second agent that needs no measurement."* — permissions:
   the agent that reads a stranger's text must not hold the tool that acts.

## Phase 2 — Mutate (8 min)

### Mutation A — *"The researcher now reads web pages instead of a table."*

Discussion first. Looking for: its tool results are now untrusted, so which tools may
it hold, and what form must its report take. Then have them add `reads_untrusted` and
run `violations`.

### Mutation B — *"Add a third worker that checks the analyst's arithmetic."*

Let them build it, then ask what it cost and how they would know it helped. The honest
answer is another two or three calls per task and a number they have not measured. A
student who says "it is more reliable" without a pass rate has not done the week.

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `report` returns the text even when the worker hit its cap | The orchestrator treats "Stopped after 6 steps" as an answer |
| Medium | pass the user's question to the worker instead of the brief | Works on easy tasks. Do they notice the worker ignored the brief? |
| Medium | remove the `try` around one parallel job | Fine until one worker fails, then every report is lost |
| Hard | count a delegation only when the worker succeeds | The limit never triggers on a worker that keeps failing |
| Nasty | give the orchestrator the `calculate` tool as well | Every test of the answer still passes. The analyst is never asked. |

The **Nasty** one is the lesson of the week in one line: the system still works, it is
no longer the design anyone thinks it is, and only the per-agent call counts show it.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Explains the handoff and its cost with their own numbers | Describes the code | Cannot say what crosses |
| **Mutate** | Names the permission boundary unprompted | Builds the change | Adds agents with no way to judge them |
| **Debug** | Goes to the delegations and the call counts | Finds it by reading code | Guesses |
| **Report** | A recommendation with the measurement that would change it | Numbers, no condition | A preference |

---

## Retro (10 min)

1. *"Did the numbers say what you expected on Monday?"*
2. *"What did your orchestrator leave out of its briefs before you fixed the prompt?"*
3. *"What did I explain badly?"*

---

## Instructor: framing week 12

Week 12 is Project 3 and the last build week. Say this:

> **Everything from here is about being hired.** Week 12 puts a system on the public
> internet with tracing and evals, week 13 is interviews, week 14 is applications. The
> code gets less interesting and the stakes get higher.

Also worth flagging honestly: weeks 8–11 were the ones where a student could coast.
Week 12 is not — there is a deployed artifact at the end of it, and either it is
reachable or it is not.

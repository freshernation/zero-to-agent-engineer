# Week 1 — Friday defence

**One hour. No new content.** 20 minutes per student on the defence, then a shared
retro. With two students, have the second one watch the first — being watched is
part of the training, and watching someone else get stuck is unexpectedly instructive.

Students should have already run `ai/defend.md` on themselves. Ask for that transcript
first; if they haven't, that is itself a signal.

---

## Phase 1 — Explain (7 min)

Open **their** `splitter.py`. Point at lines and ask. Do not accept a narration of
what the line does — push until they say *why it is there*.

1. *"Point at the line that turns what they typed into a number. Why is that needed
   at all?"* — tests whether the str/int trap actually landed.
2. *"Why is one of these `float()` and the other `int()`?"* — tests understanding
   rather than pattern-copying.
3. *"Walk me down your if/elif/else. What happens if I type `POOR` in capitals?"* —
   they will not have handled it. The right answer is "it falls to the else and gets
   15%", not "it works".
4. *"What does `:.2f` do, and what breaks if I remove it?"* — make them predict, then
   remove it and run it.
5. *"Why is `else` the ok branch rather than `elif service == "ok"`?"* — the spec said
   unknown values become ok. Did they notice, or did they get it by accident?

**Red flags:** long pauses on their own code; describing syntax instead of intent;
"I think it's because…"; being unable to say what a variable holds.

---

## Phase 2 — Mutate (10 min)

The phase that cannot be faked. Give the change verbally, and make them **say which
lines move before they touch the keyboard.**

### Mutation A — *"Make it refuse a party size of zero."*

This is deliberately not in the spec, so their program currently crashes on it.

- Ask them first: *"What happens right now if I say zero people?"*
- Let them predict. Then run it. `ZeroDivisionError`.
- Then: *"Where does the check go, and what should it do instead?"*

Watch for **where** they put it. A check after the division is a check that never runs.
Watch also for how they stop the program — they do not have `exit()` or functions yet,
so the honest week-1 answer is to wrap the rest in an `else`. If they reach for
something off the fence, ask them to solve it with what they have. That constraint is
the exercise.

### Mutation B — *"The tip is now a flat $5, whatever the service was."*

Smaller, and it tests something different: can they see which parts of the program stop
being needed? The service question, the whole if/elif/else, and the percentage in the
output line all become dead. A student who only deletes the multiplication has not
followed the change through.

---

## Phase 3 — Break (3 min)

*"Give me an input that breaks your program. Not a guess — tell me what it will do and
why, then run it."*

Available answers: `0` people (ZeroDivisionError), `abc` for the bill (ValueError),
an empty answer (ValueError), a negative bill (no error — it just produces nonsense,
which is the more interesting one).

**The best answer names the negative bill**, because it is the failure with no error
message. That is a week-4 student thinking, in week 1. Note it if you see it.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Fluent on every line including the awkward ones | Fluent on easy lines, hesitant elsewhere | Narrates what, cannot say why |
| **Mutate** | Names the exact lines before typing, gets it right | Gets there by trial and error | Cannot locate where the change goes |
| **Break** | Predicts the failure and the reason | Finds a breaking input, guesses the cause | Believes nothing breaks it |

**Pass is 3 in every phase.** A 5 and a 1 is a fail — the 1 is what ends an interview.

Record the three numbers in `instructor/signal-sheet.md`. A fail in week 1 is not a
problem, it is information, and it is cheap here in a way it never is again.

---

## Retro (last 15 min, both students together)

Four questions. Keep it moving.

1. *"What took the longest this week, and was it the concept or the typing?"*
2. *"Which stuck-log entry is still unresolved?"* — go and resolve one, live.
3. *"What did you have to explain to yourself twice?"* — that is next week's revision.
4. *"What did I explain badly?"* — ask it every week and mean it. Every live
   explanation you gave this week is a hole in the async material; patch the worst one
   before Monday.

---

## Instructor: what to do with the result

| Result | Monday |
|---|---|
| **Green** (3+ everywhere) | Proceed. Fold their weakest phase into next week's `Test me`. |
| **Amber** (one phase at 2) | Proceed, but give them one extra mutation drill on Monday, on week-1 code. |
| **Red** (any phase at 1, or two at 2) | Do **not** start week 2 content for that student. Spend Monday's hour re-defending the same milestone after they rebuild it from scratch, from a blank file. It costs one day now and saves three weeks later. |

The instinct will be to move on and hope it resolves. It does not resolve. Week 1
weakness in conditionals becomes week 8 inability to reason about a graph's control
flow, and by then it is buried under so much new material that neither of you can see
what the real problem is.

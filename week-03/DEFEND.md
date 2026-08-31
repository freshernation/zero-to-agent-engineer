# Week 3 — Friday defence

**One hour.** 20 minutes per student, the other watching, then the retro.

New this week: **phase 3 is a live debug of a bug you planted.** Read that section
before the session — you need to seed it beforehand.

Ask for their `ai/defend.md` rehearsal transcript first.

---

## Phase 1 — Explain (6 min)

Open **their** `expenses.py` and `tracker.py`.

1. *"Why does `add_expense` return a new list instead of appending to the one it was
   given?"* — the design idea of the week. "Because the test said so" is a 1.
2. *"`expenses.py` has no `print()` in it. What would break if I put one in?"* — looking
   for: it could no longer be used by anything that is not a terminal.
3. *"Show me every place a `ValueError` could come out of your code, and who catches
   each one."* — the raise/catch pair should be in different files, and they should be
   able to say why.
4. *"Your `load_expenses` catches two exceptions. Give me a real situation that causes
   the second one."* — a half-written file, a hand-edited file. If they only say "if
   it's corrupt", push for how a file gets corrupt.
5. *"What does `if __name__ == '__main__'` do, and what breaks without it?"* — they
   should be able to say *importing it would start the program*.

**Red flags:** cannot explain the library/program split beyond "the spec said";
describes `return` and `print` as interchangeable; no idea which function raises.

---

## Phase 2 — Mutate (7 min)

**Say the change. Make them name the file, the function, and the lines — before typing.**

### Mutation A — *"Add a `delete` command that removes the most recent expense."*

What you are grading is **where they put it**. The right answer has two parts:

1. A new function in `expenses.py` — `remove_last(expenses)` — returning a **new** list
   and doing no printing
2. A new branch in `tracker.py` that calls it and prints the confirmation

A student who writes the whole thing inside `tracker.py`'s `while` loop has passed the
tests all week without understanding why there are two files. That is worth finding out
now, because week 5 onwards is entirely about which layer a thing belongs in.

Ask what `delete` should do with an empty list. There is no right answer; there is only
whether they thought about it.

### Mutation B — *"The report should show each category's share as a percentage too."*

Small. `food        $   15.75   (86.7%)`. Grading one thing: do they work the percentage
out in `by_category` (wrong — it is a display concern that needs the grand total) or in
`tracker.py` (right)? Either is defensible if they can argue it. Not being able to see
that there is a choice is the fail.

---

## Phase 3 — Debug (7 min) · **NEW**

**Before the session:** open their repo, break exactly one line, save, and say nothing.

Then hand it back:

> *"One test is failing. Find it and fix it. Talk me through what you're doing as you go."*

They may use `pytest`. They may not use an AI. You are grading the **method**, not the
speed:

- Did they run the tests first, or start guessing?
- Did they read the failure message, or scroll past it?
- Did they say what they expected before changing anything?
- Did they change **one thing** at a time?
- When a change did not help, did they put it back?

### Seeds to choose from

Pick one. Harder is not better — pick the one that probes what you suspect is weak.

| Seed | Break | What it probes |
|---|---|---|
| **Easy** | `format_expense`: change `:<20` to `:<10` | Can they read a diff of two strings |
| **Easy** | `total`: `round(..., 1)` instead of `2` | Do they look at the actual vs expected numbers |
| **Medium** | `by_category`: `totals.get(category, 1)` instead of `0` | Can they reason about an off-by-something with no traceback |
| **Medium** | `load_expenses`: delete the `except json.JSONDecodeError` branch | Only one test fails, and its name tells them the answer if they read it |
| **Hard** | `add_expense`: replace the return with `expenses.append(expense)` then `return expenses` | The failing test is about the *caller's* list, not the function — chain-of-blame reading |
| **Nasty** | `tracker.py`: change `records = do_add(records)` to `do_add(records)` | The week's whole lesson, in their own code. Add silently does nothing. |

The **Nasty** one is the best test of whether week 3 landed, and it is the same bug as
Thursday's `broken_2.py`. If they solved that on Thursday and cannot solve this on
Friday, they pattern-matched Thursday rather than understanding it — which is exactly
what this phase exists to reveal.

Put the line back afterwards, in front of them, so they see what you changed.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Argues the design, not just describes it | Describes accurately, thin on why | "Because the spec said so" |
| **Mutate** | Names file, function and lines before typing | Gets there, finds the layer by trial | Puts it all in the wrong file |
| **Debug** | Tests first, hypothesis, one change at a time | Finds it, method is scrappy | Guesses; changes several things; asks what it is |

**Pass is 3 in every phase.** Record it in the signal sheet.

---

## Retro (last 15 min)

1. *"Which was harder — writing the functions or splitting them across two files?"*
2. *"You have now met the same bug three times: `total = 0` inside the loop, `add_one`
   not returning, and today's seed. What is the one sentence that covers all three?"*
   The answer you are hoping for is something like *"a function has to hand its result
   back, and a value has to be put somewhere."*
3. *"What did I explain badly?"*

---

## Instructor: the checkpoint this week really is

Weeks 1–3 are the whole of Python. From Monday it is HTTP, models, and agents, and none
of that is a fresh start — week 5's API responses are lists of dicts, week 6's model
calls are functions with error handling, week 7's agent loop is a `while` with an
accumulator and a `try`.

So this is the last cheap moment to go back. A student at 3s across all three phases is
ready. A student who cannot debug their own code without help is not, and pushing them
into week 4 does them no favours — the material stops being about Python and they will
never get the chance to catch up on it again.

If you are going to spend a whole extra week anywhere in this course, spend it here.

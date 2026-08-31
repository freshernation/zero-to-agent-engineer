# Week 4 — Friday defence + first mock interview

**One hour is not enough this week.** Budget 90 minutes: 20 minutes of defence per
student, then 30 minutes of recorded mock interview each. Run the mocks on a different
day if you have to, but run them this week.

---

## Phase 1 — Explain (6 min)

1. *"Which of your classes did not need to be a class?"* — the week's real question.
   `Expense` is arguably a dict with validation; `Ledger` clearly earns it. Any
   defensible answer scores; "they all needed to be" scores 1.
2. *"Why does `Ledger.add` refuse anything that is not an `Expense`?"* — looking for:
   because everything downstream assumes `.amount` exists, and failing at the door
   beats failing three functions later.
3. *"Point at `__repr__`. Who calls it, and when?"*
4. *"Your `Expense.__eq__` returns `NotImplemented` for a string. Why not `False`?"*
5. *"Walk me through what `load_ledger` does with a file containing `[{ruined`."*

## Phase 2 — Mutate (7 min)

### Mutation A — *"Add a date to every expense, and make `report` cover one month."*

Grading the ripple: `Expense.__init__`, `__repr__`, `__eq__`, `save`, `load_ledger`,
the CLI's `add`, and their own tests all have to change. A student who names four or
more places before typing has genuinely understood their own design.

### Mutation B — *"`Ledger.total()` is being called in a loop over 50,000 expenses and it's slow."*

No code required — just the conversation. Looking for: it recomputes the sum every
call, and it could keep a running total updated in `add`. Then the follow-up that
matters: *"what does that cost you?"* (the total can now drift out of sync with the
list, and there is a second place to get wrong). Correct answer is that it is not worth
it here. You are grading whether they can weigh a trade-off, not whether they optimise.

## Phase 3 — Debug (7 min)

Seed one bug before they arrive, as in week 3.

| Seed | Break | Probes |
|---|---|---|
| Easy | `Ledger.total` rounds to 1dp | Reading actual vs expected |
| Medium | `categories()` drops the `sorted()` | Non-deterministic failure — does it fail every run? |
| Medium | `by_category` compares `description` instead of `category` | Reading their own filter |
| Hard | Move `self.expenses = []` out of `__init__` onto the class body | Thursday's bug in their own code |
| Nasty | `Expense.__eq__` compares only `description` | Everything passes except one test, and the reason is three files away |

The **Hard** seed is the one to reach for by default — it is `broken_2.py` in their own
project, and it separates recognising a bug from understanding it.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Argues the design and its costs | Describes accurately | "Because the spec said so" |
| **Mutate** | Names four or more affected places before typing | Finds them one at a time by running | Cannot trace the ripple |
| **Debug** | Tests first, hypothesis, one change | Finds it, scrappy method | Guesses |

Pass is 3 in every phase.

---

## Then: the first mock interview

**30 minutes, gate-1 format, recorded.** Use `ai/interviewer.md` as your question bank
if you want, but run it yourself — being interviewed by a person is the thing being
practised.

Cover:

- Two or three "what does this print" questions on week 1–2 material
- One small live-coding task, watched, no AI: *"given a list of dicts, return the
  three with the highest amount"*
- Five minutes on Project 1: what it does, why those classes, what broke
- One deliberate interruption at 90 seconds, to practise being cut off

**Do not help. Do not soften. Do not stop early because it is going badly.**

Afterwards, three things and nothing more:

1. The single answer that would have lost the offer
2. One habit to fix (filler words, burying the answer, no structure, no numbers)
3. A score out of 5 on: correctness, structure, specificity, confidence

**Save the recording.** Name it `mock-01-<name>-week04`. In week 12 you play it back
next to their tenth one, and that comparison does more for their confidence than
anything you can say to them.

---

## Retro (15 min, both students)

1. *"Which of your tests would have caught a bug, and which just ran some code?"*
2. *"Your README — would a stranger get it running in four minutes?"* Then actually
   try it, on your machine, in front of them.
3. *"What did I explain badly?"*

---

## Instructor: the bar to hold here

Project 1 is the first thing that goes in front of employers. The temptation is to let
a nearly-finished one through because the student is tired and week 5 is coming.

Do not. A repository with a broken README or a test suite that passes on empty code is
worse than no repository, because a hiring manager who opens it forms a view in about
90 seconds and never revisits it. Make them finish this one properly — it is also the
template for the two that follow, and standards set here carry.

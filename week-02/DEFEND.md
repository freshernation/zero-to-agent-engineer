# Week 2 — Friday defence

**One hour.** 20 minutes per student, the other watching, then the retro.

Week 2 is where copying starts, so the mutate phase matters more than it did last week.
Someone who assembled this report from examples can run it and cannot extend it.

Ask for their `ai/defend.md` rehearsal transcript first.

---

## Phase 1 — Explain (7 min)

Open **their** `report.py`.

1. *"Point at every variable you set up before the loop. Why does each one have to be
   there rather than inside?"* — the central idea of the week. A student who cannot
   answer this wrote the loop by imitation.
2. *"`revenue` is not in the data. Where does it come from, and why is it calculated
   inside the loop rather than after it?"*
3. *"Walk me through what `revenue_pairs` holds after the third time round the loop.
   Actual values."* — make them say `[(54.0, 'Ana'), (58.0, 'Ben'), (49.0, 'Cara')]`.
   Vagueness here means they do not really picture the data.
4. *"Why is revenue first in the tuple and the name second? What happens if you swap
   them?"* — swap it and run it. Let them watch it sort alphabetically.
5. *"`average_sale` divides by `len(SALES)`. Why not by `total_units`?"* — probes
   whether they understood the spec or just made the test pass.

**Red flags:** cannot say what a variable holds at a point in time; describes the loop
as "it goes through the list" and cannot go further; surprised by their own output when
you change something.

---

## Phase 2 — Mutate (10 min)

**Say the change. Make them name the lines before touching the keyboard.**

### Mutation A — *"Every sale now has a region. Add a revenue-by-region section."*

The big one. Give them the new data:

```python
{"name": "Ana", "units": 12, "unit_price": 4.50, "region": "North"},
```

Then: *"Add a REVENUE BY REGION section at the bottom, one line per region, and I don't
want to know in advance how many regions there are."*

This needs four separate realisations, and you are grading how many they get **before**
they start typing:

1. A new dict to accumulate into, created **before** the loop
2. The count-up pattern from Wednesday's `counts.py` — but adding revenue, not 1
3. A **second** loop after the first, over the region dict
4. `sorted()` on the region keys, or the output order changes between runs

Getting 1 and 2 is a pass. Getting 3 and 4 unprompted is a strong 5. Not seeing that
they need a second loop is the most common miss and is worth talking through.

> This is the first mutation of the course that is genuinely a small feature rather
> than a tweak. Expect it to take most of the ten minutes. That is fine.

### Mutation B — *"Rank by units sold instead of revenue."*

Small, and it tests one thing: do they know the tuple order **is** the sort order?

The right answer is that `revenue_pairs.append((revenue, name))` becomes
`append((units, name))`, and the ranking's `${revenue:.2f}` formatting has to change
too because units are not money. A student who only changes the first part and leaves
`$` in the output has not followed the change through — same failure as last week's
flat-tip mutation, which is worth naming out loud to them.

---

## Phase 3 — Break (3 min)

*"Give me a specific input that breaks this. Predict what happens, then run it."*

Available answers, weakest to strongest:

- An empty `SALES` list → `ZeroDivisionError` on the average, and `IndexError` on the ranking
- Fewer than three sales → `IndexError` in the top-3 loop. **This is the good answer** —
  it is the one a real dataset actually produces, and it is invisible until it happens
- Two people with identical revenue → the tie breaks by name in reverse, which is not
  wrong exactly, but is not what anyone would want. A student who raises this
  unprompted has read Thursday's note properly and is thinking like an engineer

---

## Scoring

Same table and same bar as week 1: **3 in every phase.** Record it in the signal sheet.

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Says what every variable holds and when | Fluent on the loop, vague on the tuples | Narrates, cannot picture the data |
| **Mutate** | Names the lines and the second loop before typing | Gets there by trial and error | Cannot see where a new accumulator goes |
| **Break** | Names the fewer-than-three case or the tie | Finds the empty list | Believes nothing breaks it |

---

## Retro (last 15 min)

1. *"Which of the three — before, during, after the loop — did you get wrong most?"*
2. *"Where did you nearly reach for an AI this week, and what did you do instead?"*
3. *"What did I explain badly?"*

---

## Instructor: the week-2 specific worry

A red here is more serious than a red in week 1. Loops and dicts are load-bearing for
everything that follows — week 5's API responses are lists of dicts, week 7's agent
loop is a `while` with an accumulator, and week 9's retrieval results are ranked tuples.
Every one of those is this week's material wearing a different hat.

If a student cannot mutate this report on Friday, do not start week 3 for them. Give
them Monday to rebuild the whole milestone from a blank file with the spec beside them,
then re-defend it Tuesday. One day now; three weeks later.

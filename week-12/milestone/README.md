# Week 12 Milestone — Ten Mocks, Scored

> Ten recorded interviews, scored on one rubric, next to the one you did in week 4.

---

## The files

| File | Holds |
|---|---|
| `scores.py` | `BASELINE` (week 4) and `MOCKS` (this week), plus the arithmetic |
| `MOCK_LOG.md` | One entry per mock — what was asked, what went wrong |
| `PROGRESS.md` | **The comparison.** Week 4 against week 12. |

---

## The ten

Across all five gates, at least one each, spread through the week. Your instructor runs
some; use `ai/interviewer.md` for the rest.

**Record every one.** Name them `mock-NN-<name>-week12`.

Score each on four dimensions, 1 to 5:

| Dimension | 5 | 1 |
|---|---|---|
| **Correctness** | right, and knows the edges | wrong, or would not run |
| **Structure** | answer first, then the detail | rambles, buries it |
| **Specificity** | numbers, names, real examples | "it was quite fast" |
| **Confidence** | plain, unhedged, takes a position | hedges everything, trails off |

Be hard on yourself. An inflated log is worse than none, because it hides the two things
you would otherwise have fixed.

## `scores.py`

| Thing | Is |
|---|---|
| `BASELINE` | your week-4 mock's four scores |
| `MOCKS` | the ten, each with `number`, `gate`, and the four dimensions |
| `mean_of(mock)` | the average of the four, 2dp |
| `overall(mocks)` | the average across all of them, 2dp |
| `by_gate(mocks)` | `{gate: mean}` |
| `weakest_dimension(mocks)` | the lowest-scoring of the four, across all mocks |
| `improvement(baseline, mocks)` | overall minus the baseline mean, 2dp |
| `trend(mocks)` | `(first_five_mean, last_five_mean)` |

## `MOCK_LOG.md`

One `## Mock NN` section each, with:

- **Gate** and who ran it
- **The question that went worst**, quoted
- **What a better answer was** — bullets you could have said, not a script
- **One habit to fix**

## `PROGRESS.md`

| Section | What goes in it |
|---|---|
| `## The baseline` | What week 4 was actually like. Be honest; nobody's was good. |
| `## What the numbers say` | Baseline, overall, the improvement, the trend. Real figures. |
| `## What actually changed` | Not the score — the behaviour. What do you do differently now? |
| `## What is still weak` | The weakest dimension and your plan for it |

At least 350 words, with at least four numbers.

---

## Friday: watch the tapes

The last thirty minutes of the week. Play your week-4 mock, then your tenth.

Nobody enjoys the first one. That is the point — it is evidence rather than
reassurance, and evidence is what actually changes how you walk into a room.

---

## Check it

```bash
pytest week-12/milestone -v
```

---

## Ship it

```bash
git add -A && git commit -m "week 12: ten mocks, scored" && git push
```

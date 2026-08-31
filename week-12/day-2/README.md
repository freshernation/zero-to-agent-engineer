# Day 2 — Writing Python while somebody watches

> **By the end of today** you can solve a small problem correctly, out loud, in under
> ten minutes.

---

## What you need to know

### The screen is not about cleverness

A junior coding screen is checking three things, and none of them is whether you know a
trick:

1. Can you turn a problem into steps
2. Do you handle the empty case, the one-item case, and the tie
3. Do you keep talking

Week 1's decomposition, week 3's edge cases, and a skill you have not practised.

### Talk the whole time

Silence reads as being stuck even when you are thinking. Narrate:

> *"Right — I need the most common word. So: split it, count them, find the maximum.
> Ties, I'll take the alphabetically first. Let me start with the counting..."*

That sentence has already told the interviewer you can decompose, that you spotted the
tie case, and where you are going. It costs ten seconds.

### Say the edge cases before you are asked

Empty input. One item. All the same. A tie. Saying *"what should this do with an empty
list?"* out loud is worth more than the solution, because it is the thing juniors
reliably do not do.

### Write the obvious version first

The clear loop, then say *"there's a comprehension version of this if you'd prefer"*.
Starting with the clever one and getting stuck is much worse than starting plainly and
finishing.

### If you are stuck

Say what you have tried and what you would try next. An interviewer will help a
candidate who is thinking out loud. Nobody can help silence.

---

## The drills

Ten problems in `drills.py`. Each has a **target time**. Do them the way you would in an
interview:

- start a timer
- **talk out loud**, alone, to the wall
- no AI, no searching
- when the timer ends, stop and note where you got to

```bash
python3 week-12/day-2/drill.py            # list them
python3 week-12/day-2/drill.py two_sum    # run one, timed
pytest week-12/day-2 -v                   # grade them all
```

| # | Function | Target |
|---|---|---|
| 1 | `two_sum(numbers, target)` | 6 min |
| 2 | `most_common_word(text)` | 6 min |
| 3 | `group_by(records, key)` | 5 min |
| 4 | `top_n_by(records, key, n)` | 5 min |
| 5 | `running_total(numbers)` | 4 min |
| 6 | `chunk(items, size)` | 5 min |
| 7 | `first_duplicate(items)` | 5 min |
| 8 | `invert(mapping)` | 5 min |
| 9 | `is_balanced(text)` | 8 min |
| 10 | `flatten(nested)` | 7 min |

Every one is week 1–4 material. If any feels impossible, that is the most useful thing
you will learn today — go back to that week for an hour rather than pushing on.

### After each drill

Write one line in `DRILL_LOG.md`: which one, how long it actually took, and what slowed
you down. By Friday that log tells you exactly which two to practise again.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 12 day 2" && git push
```

---

## Predict-then-run

Do `two_sum` twice: once in silence, once narrating out loud to an empty room.

Time both. Most people are slower out loud the first time and faster by the third — and
in the interview you do not get a silent option.

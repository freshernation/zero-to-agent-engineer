# Week 1 Milestone — The Bill Splitter

> Everything you learned this week, in one program you wrote yourself.

A group finishes a meal. Your program works out the tip, the total, and what each
person owes.

---

## What it must do

Ask three questions, **in this order**, with **exactly** this prompt text:

```
Bill total:
Number of people:
Service (good/ok/poor):
```

Work out the tip from the service rating:

| Service | Tip |
|---|---|
| `good` | 20% |
| `ok` | 15% |
| `poor` | 10% |
| anything else | treat it as `ok` |

Then print exactly three lines:

```
Tip (20%): $12.00
Total: $72.00
Each person pays: $18.00
```

- The tip line shows **the percentage that was applied**, in brackets.
- All three money amounts have **exactly two decimal places**.
- `Total` is the bill plus the tip.
- `Each person pays` is the total divided by the number of people.

### Worked example

Bill `60`, `4` people, service `good` → 20% of 60 is 12.00, total is 72.00,
each person pays 18.00. That is the output above.

---

## Check it

```bash
pytest week-01/milestone -v
```

Nine tests. All nine green before you go any further.

---

## Then make it good

Green tests mean it behaves correctly. They say nothing about whether the code is any
good, and on Friday you will be asked about the code, not the output.

Open `ai/editor.md` in a fresh chat, paste this spec, paste your code, and work through
what it finds. Expect it to find things. Specifically, before Friday:

- [ ] Every variable name says what it holds. No `x`, `n`, `t`, `temp`.
- [ ] The tip rates are in variables, not typed into the middle of a calculation.
- [ ] A short comment at the top saying what the program does and who wrote it.
- [ ] You can read the whole thing top to bottom without backtracking.
- [ ] You could explain **every single line** to someone who has never seen it.

That last one is not a suggestion. It is Friday's exam.

---

## Ship it

```bash
git add -A
git commit -m "week 1 milestone: bill splitter"
git push
```

---

## Friday

Two defences, in this order:

1. **Rehearsal.** Run `ai/defend.md` on your own code first. Paste this spec, paste
   your code. It will score you out of 5 on three phases. Do this *before* the live
   hour, not during.
2. **The real one.** Your instructor runs the same three phases, live, and will change
   the requirements while you watch.

You pass at 3 out of 5 in every phase. Not on average — a 5 and a 1 is a fail, because
the 1 is the thing that ends an interview.

> **One honest warning about phase 2.** Your instructor is going to change a rule and
> ask which lines move. Almost everyone can narrate code they did not really write.
> Almost nobody can modify it. If you have leaned on the AI this week more than the
> rules allowed, Friday is where that becomes visible — and it is much better that it
> becomes visible in week 1, in a room with two people in it, than in week 13 in front
> of someone with a job to give away.

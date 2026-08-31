# Week 2 Milestone — The Sales Report

> Ten records in. A formatted report out. Nothing typed in by hand.

This is `records.py` from Wednesday with more columns, real arithmetic, and a ranking.
It is also the first program you will write that would be genuinely tedious to do by
hand — which is the point of the whole week.

---

## The data

`report.py` already contains this. **Do not change it, and do not reformat it** — the
tests swap it for a different set of sales to check your program works the numbers out
rather than containing them.

```python
SALES = [
    {"name": "Ana",  "units": 12, "unit_price": 4.50},
    {"name": "Ben",  "units": 8,  "unit_price": 7.25},
    ...
]
```

Each record has a `name`, a `units` count, and a `unit_price`. A person's **revenue**
is their units times their unit price. That number is not in the data — you work it out.

---

## The output

Exactly this, for the data as given:

```
SALES REPORT
========================================
Ana           12 x $4.50 = $54.00
Ben            8 x $7.25 = $58.00
Cara          20 x $2.45 = $49.00
Dev            5 x $12.00 = $60.00
Eve           15 x $3.20 = $48.00
Finn           9 x $6.50 = $58.50
Gita          25 x $1.80 = $45.00
Hugo           7 x $9.00 = $63.00
Iris          11 x $5.50 = $60.50
Jon           18 x $2.75 = $49.50
========================================
Total units:   130
Total revenue: $545.50
Average sale:  $54.55
Best seller:   Hugo ($63.00)

TOP 3 BY REVENUE
1. Hugo         $63.00
2. Iris         $60.50
3. Dev          $60.00
```

### The formatting rules

| Part | Rule |
|---|---|
| Rules | 40 `=` characters |
| Record line | `{name:<12} {units:>3} x ${price:.2f} = ${revenue:.2f}` |
| Ranking line | `{rank}. {name:<12} ${revenue:.2f}` |
| Money | Always two decimal places |
| `Average sale` | Total revenue divided by **how many records there are** |
| `Best seller` | Highest revenue, not most units |
| Blank line | One, between `Best seller` and `TOP 3` |

---

## How to approach it

Do not start typing. Take five minutes and write the steps in English first — this is
the same drill your instructor ran on Thursday and it is worth more than any hint:

1. What do you need before the loop starts?
2. What happens once per record inside it?
3. What can only be worked out after the loop has finished?

Almost every bug in this milestone is a step in the wrong one of those three places.

For the ranking, use Thursday's tuple trick. Build `(revenue, name)` pairs as you go
through the main loop — you are already working revenue out there, so do not loop twice.

---

## Check it

```bash
pytest week-02/milestone -v
```

Twelve tests. Four of them run your file against a **different** set of sales, so
anything you typed in by hand will show up immediately.

---

## Then make it good

Green tests say it behaves. Friday is about the code. Run `ai/editor.md` on it, and
before the defence:

- [ ] Names say what they hold. `total_revenue`, not `t` or `total2`.
- [ ] One loop over `SALES`, not three.
- [ ] No number in your code that appears in the output — every figure is calculated.
- [ ] You can say, for every variable, whether it is set before, during, or after the
      loop, and why it has to be there.

That last one is Friday's first question.

---

## Ship it

```bash
git add -A
git commit -m "week 2 milestone: sales report"
git push
```

---

## Friday

Rehearse with `ai/defend.md` first, then the live defence. Same three phases, same bar:
**3 out of 5 in every one.**

You already know one of the mutations is coming — the spec has an obvious gap in it, and
your instructor is going to ask for the thing that is missing. Do not pre-build it.
Being able to *find* where a change goes, under pressure, on code you wrote three days
ago, is the whole skill being measured.

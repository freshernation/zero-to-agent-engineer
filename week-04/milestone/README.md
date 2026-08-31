# Project 1 — The Expense Tracker

> Week 3's tracker, rebuilt around classes, with your own tests and a README.
> **This one goes on GitHub and stays there.**

The first of the three projects that get you interviewed. It is small, and that is
correct: a hiring manager reads whether it is **finished**. Tests that run, a README
that works, commits that tell a story. Half-finished ambitious projects lose to small
complete ones every time.

---

## The files you write

| File | What it holds |
|---|---|
| `expense.py` | The `Expense` class |
| `ledger.py` | The `Ledger` class and `load_ledger` |
| `cli.py` | The program a person runs |
| `test_ledger.py` | **Your** test suite |
| `PROJECT_README.md` | **Your** README |

Same rule as week 3, now enforced by tests: `expense.py` and `ledger.py` never print
and never ask. All of that lives in `cli.py`.

---

## `expense.py`

**`Expense(description, amount, category)`**

- attributes: `description`, `amount`, `category`
- raises `ValueError("Description cannot be empty")` for an empty description
- raises `ValueError("Amount must be positive")` for zero or less
- `__repr__` → `Expense('Coffee', 4.5, 'food')`
- `__eq__` → equal when all three match; `NotImplemented` against anything else

## `ledger.py`

**`Ledger()`** — starts empty.

| Member | Does |
|---|---|
| `add(expense)` | appends it; raises `TypeError("Can only add Expense objects")` for anything else |
| `total()` | every amount, rounded to 2dp |
| `by_category(category)` | the expenses in that category, in the order added |
| `categories()` | every category present, sorted, no repeats |
| `biggest()` | the largest `Expense`, or `None` when empty |
| `__len__` | how many |
| `__repr__` | `Ledger(3 expenses, $17.75)` |
| `save(path)` | writes the ledger as JSON |

**`load_ledger(path)`** — a module-level function returning a `Ledger`. An empty one if
the file is missing or damaged.

## `cli.py`

The week-3 command loop, now driving objects. Loads `expenses.json` at the start,
saves on quit, prompts with `> `.

| Command | Output |
|---|---|
| `add` | asks Description / Amount / Category, then `Added: Coffee $4.50 (food)` |
| `list` | `Coffee              food        $    4.50` per expense, or `No expenses yet.` |
| `total` | `Total: $6.50` |
| `report` | `food        $    4.50` per category, alphabetical, or `No expenses yet.` |
| `quit` | `Saved 1 expense.` / `Saved 2 expenses.` |
| anything else | `Unknown command: banana` |

A rejected `Expense` prints the `ValueError`'s message and abandons that `add`:

```
> add
Description: Coffee
Amount: -5
Category: food
Amount must be positive
```

All three questions are asked first, then the `Expense` is built — and it is the
`Expense` class that decides whether the values are acceptable. Keeping that judgement
in one place is the point of having the class at all.

---

## `test_ledger.py` — your suite

At least **twelve** test functions, at least **two** `pytest.raises`, and at least one
`@pytest.mark.parametrize`.

It gets graded three ways:

1. It must **pass** against your own code.
2. It must **fail** against an implementation where every method does nothing.
3. It must **fail** against an implementation where every method returns a plausible
   constant — `total()` always `0.0`, `by_category()` always `[]`, and no validation
   at all.

Numbers 2 and 3 are the whole point. A suite that goes green on code that does nothing
has not tested anything; it has just run some code. Very few junior candidates have
ever had this pointed out to them, and being able to talk about it is worth more in an
interview than another feature would be.

```bash
python3 week-04/milestone/check_my_tests.py     # run your suite and see the output
pytest week-04/milestone -v                     # grade everything
```

---

## `PROJECT_README.md` — your README

The five sections, in this order. Write for someone who has never seen it and has four
minutes.

1. **What it is** — one sentence
2. **What it does** — three or four bullets
3. **How to run it** — commands they can paste
4. **How to run the tests** — the line that says this is real
5. **What you would do next** — honest and brief

There is a test that checks all five headings exist and that it is more than 150 words.
That test cannot tell whether it is any *good* — your instructor will, on Friday, and so
will everyone who opens your GitHub.

---

## Ship it

```bash
git add -A
git commit -m "project 1: expense tracker"
git push
```

Then look at your repository the way a stranger would. Does the README explain it? Do
the commands work if you paste them? Does the commit history read like someone building
something, or like one enormous "stuff" commit?

---

## Friday

Three-phase defence on this code, then **your first mock interview** — 30 minutes,
gate-1 format, recorded.

It will go badly. That is the point: that tape is the baseline you get played back
against in week 12, and the gap between the two is where your confidence actually comes
from. Nobody has ever felt good about their first one.

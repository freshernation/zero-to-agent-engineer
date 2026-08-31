# Week 3 Milestone — The Expense Tracker

> Two files. Saves to disk. Cannot be crashed by anything a person types.

This is the first thing you will build that is recognisably a **program** rather than
an exercise. It has a library, a user interface, persistent storage, and error
handling — which is the shape of most software you will ever be paid to write.

---

## The two files

| File | What it is | Rule |
|---|---|---|
| `expenses.py` | The logic. Seven functions. | **Never prints. Never asks. Never crashes on its own.** |
| `tracker.py` | The program a person uses. | Does all the printing and asking. |

That split is the whole design. `expenses.py` could be used by a website, a phone app,
or a test suite without changing a line — because it only takes values in and hands
values back. Keep it that way; there is a test that checks it.

---

## `expenses.py`

An expense is a dict with exactly three keys:

```python
{"description": "Coffee", "amount": 4.5, "category": "food"}
```

| Function | Returns / raises |
|---|---|
| `parse_amount(text)` | the amount as a `float`, or raises `ValueError` |
| `add_expense(expenses, description, amount, category)` | a **new list** with the expense on the end |
| `total(expenses)` | the sum of all amounts, rounded to 2dp |
| `by_category(expenses)` | a dict of category to its total, each rounded to 2dp |
| `format_expense(expense)` | one display line (format below) |
| `load_expenses(path)` | the saved list, or `[]` if the file is missing or damaged |
| `save_expenses(path, expenses)` | nothing — writes the list as JSON |

`parse_amount` raises with these exact messages, same as Tuesday:

- not a number → `Amount must be a number`
- negative → `Amount cannot be negative`

### `add_expense` returns a *new* list

It must not change the list it was given:

```python
first = []
second = add_expense(first, "Coffee", 4.5, "food")
len(first)      # still 0
len(second)     # 1
```

This is deliberate, and there is a test for it. A function that quietly modifies
something you handed it is the hardest kind of bug to find later — the caller has no
idea anything happened. Take values in, hand new ones back.

### `format_expense`

```
{description:<20}{category:<12}${amount:>8.2f}
```

```
Coffee              food        $    4.50
Monthly train pass  transport   $   89.00
```

---

## `tracker.py`

Loads `expenses.json` when it starts, saves it when you quit. Prompts with `> `.

| Command | Does |
|---|---|
| `add` | asks three questions, then confirms |
| `list` | one line per expense |
| `total` | the grand total |
| `report` | totals per category, **in alphabetical order** |
| `quit` | saves and stops |
| anything else | `Unknown command: xyz` |

### A whole session

```
> add
Description: Coffee
Amount: 4.50
Category: food
Added: Coffee $4.50 (food)
> add
Description: Bus
Amount: 2.00
Category: transport
Added: Bus $2.00 (transport)
> list
Coffee              food        $    4.50
Bus                 transport   $    2.00
> total
Total: $6.50
> report
food        $    4.50
transport   $    2.00
> quit
Saved 2 expenses.
```

The report line is `{category:<12}${amount:>8.2f}`.

### When it goes wrong

```
> add
Description: Coffee
Amount: abc
Amount must be a number
> add
Description: Refund
Amount: -5
Amount cannot be negative
> banana
Unknown command: banana
> list
No expenses yet.
> quit
Saved 0 expenses.
```

A bad amount **abandons that `add`** and goes back to the prompt. It does not ask
again, and it does not add anything.

`list` and `report` both say `No expenses yet.` when there is nothing.

`quit` says `Saved 1 expense.` for exactly one, and `Saved N expenses.` otherwise.

---

## Check it

```bash
pytest week-03/milestone -v
```

Twenty-nine tests. Most call `expenses.py` directly; the rest run `tracker.py` and type
commands into it, including a test that runs it twice to prove the data survived.

---

## Then make it good

Green tests say it behaves. Friday is about the code.

- [ ] `expenses.py` has no `print()` and no `input()` anywhere in it
- [ ] `tracker.py` does no arithmetic and no file handling of its own
- [ ] Every function in `expenses.py` has a docstring saying what it **returns**
- [ ] `tracker.py`'s command handling is readable top to bottom
- [ ] Nothing a person can type produces a traceback

Run `ai/editor.md` over both files before Friday.

---

## Ship it

```bash
git add -A
git commit -m "week 3 milestone: expense tracker"
git push
```

---

## Friday

The defence has a new third phase this week. Your instructor will **break one line of
your own code** before the session and hand it back, and you debug it live while they
watch.

You cannot revise for this and you should not try. Everything you have done on the four
Thursdays of this course has been preparation for it.

# Day 2 — Objects that print, compare, and contain

> **By the end of today** your objects behave like the built-in types do, and one class
> can be built out of others.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on __repr__ and __eq__ — 20 min]`
- [ ] `[INSTRUCTOR: source on composition — 15 min]`

---

## What you need to know

### `__repr__` — how your object looks

By default, printing an object is useless:

```python
print(Point(3, 4))          # <__main__.Point object at 0x104a2b1d0>
```

That memory address will waste hours of your life during debugging. Fix it once, on
the class:

```python
    def __repr__(self):
        return f"Point(3, 4)"           # no - hard-coded
        return f"Point({self.x}, {self.y})"     # yes
```

```python
print(Point(3, 4))          # Point(3, 4)
print([Point(1, 2)])        # [Point(1, 2)]     <- works inside containers too
```

**The convention: `__repr__` should look like the code that would recreate the
object.** `Point(3, 4)` is right; `A point at 3, 4` is not. Follow it — every Python
programmer expects it, and it means you can paste the output straight back into a
prompt to reproduce a bug.

Write `__repr__` on **every** class you make. It costs one line and it is the single
highest-return habit in this week.

### `__eq__` — how your object compares

```python
Point(3, 4) == Point(3, 4)      # False by default!
```

By default, two objects are equal only if they are *the same object in memory*. For a
`Point` that is almost never what you want:

```python
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

```python
Point(3, 4) == Point(3, 4)      # True
Point(3, 4) in [Point(3, 4)]    # True - `in` uses __eq__ too
```

Being careful, `other` might not be a `Point` at all:

```python
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y
```

`NotImplemented` is Python's way of saying *"I do not know how to compare these"*,
which lets it fall back to its default answer of `False`. Returning `False` yourself
looks the same today and does the wrong thing later.

### `__len__`

```python
    def __len__(self):
        return len(self.expenses)
```

Now `len(ledger)` works. Add it whenever "how many" is an obvious question about your
object, and never as a way of returning something that is not a count.

### Composition — objects made of objects

```python
class Expense:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount


class Ledger:
    def __init__(self):
        self.expenses = []

    def add(self, expense):
        self.expenses.append(expense)

    def total(self):
        return sum(e.amount for e in self.expenses)
```

A `Ledger` **has** `Expense`s. That is composition, and it is how the overwhelming
majority of real object design works. You will hear a lot about inheritance; you will
use composition ten times as often.

Notice that `Ledger.total()` does not know how an `Expense` stores its amount — it just
asks. Each class minds its own business, and that is what makes them replaceable.

### The question to keep asking

> **Does this need to be a class?**

A class earns its place when state and behaviour travel together. If yours has one
method and no state, you have written a function and put a costume on it. That is not a
disaster — it is just worth noticing, and Friday will ask you about it.

---

## Exercises

```bash
pytest week-04/day-2 -v
```

### 1. `point.py`

`Point(x, y)` with attributes `x` and `y`, plus:

| Method | Returns |
|---|---|
| `__repr__` | `Point(3, 4)` |
| `__eq__` | equal when both coordinates match; `NotImplemented` for anything not a `Point` |
| `distance_to(other)` | straight-line distance, rounded to 2dp |
| `move(dx, dy)` | nothing — shifts this point |

Distance is `((x2-x1)**2 + (y2-y1)**2) ** 0.5`. No imports needed.

### 2. `ledger.py`

Two classes.

**`Expense(description, amount, category)`** — three attributes, and a `__repr__` of
`Expense('Coffee', 4.5, 'food')`. Note the quotes around the strings — use `!r` in
your f-string and Python does it for you.

**`Ledger()`** — starts empty, holds `Expense` objects:

| Method | Does |
|---|---|
| `add(expense)` | appends it |
| `total()` | every amount, rounded to 2dp |
| `by_category(category)` | a list of the expenses in that category |
| `biggest()` | the single largest `Expense`, or `None` when empty |
| `__len__` | how many expenses |
| `__repr__` | `Ledger(3 expenses, $17.75)` |

### 3. `deck.py`

**`Card(rank, suit)`** — `__repr__` of `Card('A', 'spades')`, and `__eq__`.

**`Deck(cards)`** — takes a list of `Card`s:

| Method | Does |
|---|---|
| `deal(n)` | returns the first `n` cards **and removes them**; raises `ValueError("Not enough cards")` if there are too few |
| `add(card)` | puts one on the bottom |
| `__len__` | how many are left |
| `__repr__` | `Deck(52 cards)` |

`deal` is the interesting one: it has to change the deck *and* return something. Get
the order right — a deal that removes the cards and then fails leaves you worse off
than one that fails first.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 4 day 2" && git push
```

---

## Predict-then-run

```python
class Bag:
    contents = []                   # note: NOT inside __init__

    def add(self, item):
        self.contents.append(item)

a, b = Bag(), Bag()
a.add("apple")
print(b.contents)
```

This is the most confusing bug in beginner Python and it caught you on Monday's
`test_two_inventories_are_separate`. Work out with the tutor **why** `b` has an apple
in it, and what the one-line fix is.

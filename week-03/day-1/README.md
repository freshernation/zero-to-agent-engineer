# Day 1 — Functions

> **By the end of today** you can package a piece of logic under a name, hand it
> inputs, and get an answer back.

---

## Read / watch first

- [ ] [**Defining and calling functions**](../../content/week-03/day-1/defining-and-calling-functions.md) — 30 min · docs: [Defining Functions](https://docs.python.org/3.14/tutorial/controlflow.html#defining-functions)
- [ ] [**Return values and scope**](../../content/week-03/day-1/return-values-and-scope.md) — 20 min · docs: [Scopes and Namespaces](https://docs.python.org/3.14/tutorial/classes.html#python-scopes-and-namespaces)

---

## What you need to know

### Defining one

```python
def add_tax(amount):
    return amount * 1.08
```

- `def` starts the definition, the name is yours to choose
- `amount` is a **parameter** — a variable that only exists inside this function
- the colon and indent, again, exactly like `if` and `for`
- `return` hands a value back to whoever called it

Defining a function runs nothing. It is a recipe sitting on a shelf. **Calling** it is
what cooks:

```python
total = add_tax(100)        # now it runs. total is 108.0
```

### `return` is not `print` — read this bit twice

This is the mistake almost everyone makes today, and it is worth twenty minutes of
your attention now rather than an hour of confusion on Friday.

```python
def add_tax_wrong(amount):
    print(amount * 1.08)        # shows a number on screen

def add_tax_right(amount):
    return amount * 1.08        # hands a number BACK
```

They look identical when you run them. They are completely different:

```python
a = add_tax_wrong(100)      # prints 108.0, and a is None
b = add_tax_right(100)      # prints nothing, and b is 108.0

print(a + 10)               # TypeError - you cannot add 10 to None
print(b + 10)               # 118.0
```

A function that prints has **shown** you the answer. A function that returns has
**given** it to you. Only the second one can be used by other code — and other code is
the entire point of writing functions.

> **A function with no `return` hands back `None`.** Python does not warn you. You find
> out later, somewhere else, with a `TypeError` that points at a line where nothing is
> wrong. That is Thursday's `broken_1.py`, and it is coming.

**Rule for this week: your functions return, and your `print()` calls live outside
them.** There is one exception — a function whose entire job is displaying something —
and you will know when you have written one.

### Several parameters, and returning early

```python
def split_bill(total, people):
    if people <= 0:
        return 0                # stops here, hands back 0
    return total / people       # only reached if people > 0
```

`return` ends the function immediately. Everything after it in that call is skipped.
Using that to handle the awkward case first, then getting on with the real work, keeps
your functions flat and readable.

### Default arguments

```python
def add_tax(amount, rate=0.08):
    return amount * (1 + rate)

add_tax(100)              # 108.0     uses the default
add_tax(100, 0.20)        # 120.0     overrides it
add_tax(100, rate=0.20)   # 120.0     same, but says what the number means
```

Parameters with defaults must come after ones without. Naming the argument at the call
site — `rate=0.20` — costs nothing and stops `add_tax(100, 0.20)` from being a mystery
to whoever reads it next, including you.

### Scope — what happens inside stays inside

```python
def calculate():
    subtotal = 50           # exists only while this function runs
    return subtotal

print(subtotal)             # NameError - it is gone
```

And the version that catches people out, because there is no error at all:

```python
count = 0

def increment():
    count = count + 1       # UnboundLocalError, and not what you meant anyway

def increment_properly(count):
    return count + 1        # take it in, hand it back. This is the way.
```

A function should take what it needs as parameters and hand back what it produced.
Reaching outside itself is how you get bugs that only appear when things run in a
different order.

### Docstrings

```python
def split_bill(total, people):
    """Return each person's share of a bill, rounded to 2 decimal places."""
    return round(total / people, 2)
```

A sentence, in triple quotes, on the first line of the function. Say what it
**returns**, not how it works — the code already says how.

### Functions calling functions

```python
def price_label(amount):
    return f"${amount:.2f}"

def summary_line(name, amount):
    return f"{name:<12} {price_label(amount)}"
```

`summary_line` does not know how a price is formatted, and does not need to. Change
`price_label` once and everything that uses it changes too. **That is the whole reason
functions exist**, and it is what today is really teaching.

---

## Exercises

Every file today **only defines functions**. No `input()`, no top-level `print()` —
the tests import your file and call the functions directly.

```bash
pytest week-03/day-1 -v
```

### 1. `money.py`

| Function | Returns |
|---|---|
| `add_tax(amount, rate=0.08)` | `amount` plus tax, rounded to 2 decimal places |
| `apply_discount(price, percent)` | `price` with `percent` taken off, rounded to 2dp |
| `split_bill(total, people)` | each person's share, rounded to 2dp |

```python
add_tax(100)              # 108.0
add_tax(100, 0.20)        # 120.0
add_tax(49.99)            # 53.99
apply_discount(50, 10)    # 45.0
split_bill(100, 3)        # 33.33
```

Use `round(value, 2)`. Give each one a docstring.

### 2. `grades.py`

| Function | Returns |
|---|---|
| `letter_grade(score)` | `"A"` `"B"` `"C"` `"D"` or `"F"` — same bands as week 1 |
| `average(scores)` | the mean of a list, rounded to 1 decimal place |
| `highest(scores)` | the biggest score |
| `count_passing(scores, threshold=60)` | how many scores are at or above the threshold |

```python
letter_grade(90)                    # "A"
average([90, 80, 70])               # 80.0
count_passing([50, 60, 90])         # 2
count_passing([50, 60, 90], 70)     # 1
```

### 3. `labels.py`

| Function | Returns |
|---|---|
| `price_label(amount)` | `"$4.50"` — a string, two decimal places |
| `initials(first, last)` | `"A.S."` — first letters, each followed by a dot |
| `summary_line(name, amount)` | the name left-aligned in 12, a space, then the price label |

```python
price_label(4.5)                    # "$4.50"
initials("Ana", "Silva")            # "A.S."
summary_line("Ana", 4.5)            # "Ana          $4.50"
```

**`summary_line` must call `price_label`** rather than formatting the money itself.
There is a test that checks this, by swapping `price_label` for a different one and
making sure `summary_line` changes too.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 3 day 1" && git push
```

---

## Predict-then-run

```python
def double(n):
    print(n * 2)

result = double(5)
print(result)
print(result + 1)
```

Three lines of output, and the last one is an error. Say what each line does *before*
you run it. If you can explain all three, today has landed.

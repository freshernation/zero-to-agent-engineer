# Day 3 — Decisions

> **By the end of today** your program can take different paths depending on what it
> was given.

Days 1 and 2 ran top to bottom, every line, every time. Today that stops. This is the
day programs start being interesting — and the day you first have to think about the
cases you did *not* have in mind.

---

## Read / watch first

- [ ] [**`if` / `elif` / `else`**](../../content/week-01/day-3/if-elif-else.md) — 25 min · docs: [`if` Statements](https://docs.python.org/3.14/tutorial/controlflow.html#if-statements)
- [ ] [**Boolean logic — `and`, `or`, `not`**](../../content/week-01/day-3/boolean-logic.md) — 15 min · docs: [Boolean Operations](https://docs.python.org/3.14/library/stdtypes.html#boolean-operations-and-or-not)

---

## What you need to know

### Comparison gives you `True` or `False`

```python
print(5 > 3)        # True
print(5 == 3)       # False
```

**`=` assigns. `==` compares.** Getting these confused is the single most common
beginner bug and it will happen to you today.

| | |
|---|---|
| `==` | equal to |
| `!=` | not equal to |
| `<` `>` | less / greater than |
| `<=` `>=` | less / greater than or equal to |

### `if`

```python
temperature = 31

if temperature > 30:
    print("Hot")
```

Two things that are not decoration:

1. **The colon** at the end of the `if` line.
2. **The indentation** — four spaces. In most languages indentation is a courtesy. In
   Python it *is* the structure: it is how Python knows what belongs inside the `if`.
   Get it wrong and you get an `IndentationError`, or worse, code that runs and does
   the wrong thing.

### `elif` and `else`

```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

**Order matters enormously.** Python checks top to bottom and stops at the first match.
If you put `score >= 80` first, a score of 95 gets a B — it matched, and Python never
looked at the rest. Read your conditions in order and ask what a 95 does.

### `and`, `or`, `not`

```python
if age >= 18 and has_ticket:
    print("Come in")

if day == "Saturday" or day == "Sunday":
    print("Weekend")
```

- `and` — **both** sides must be true
- `or` — **either** side is enough
- `not` — flips it

A trap worth meeting now:

```python
if day == "Saturday" or "Sunday":     # always True. Always.
```

`"Sunday"` on its own is not a comparison — it is just a non-empty piece of text, which
Python treats as true. You have to say `day == "Saturday" or day == "Sunday"`. Write out
both comparisons in full, every time.

### Nesting

An `if` can live inside another `if`. Indent one more level:

```python
if is_member:
    if spend > 100:
        print("Free delivery")
```

Often the same thing reads better as `and`. Prefer the flatter version when you can.

---

## Exercises

```bash
pytest week-01/day-3 -v
```

### 1. `grade.py`

Ask `Score: `, then print `Grade: A` (or B, C, D, F).

| Score | Grade |
|---|---|
| 90 and above | A |
| 80–89 | B |
| 70–79 | C |
| 60–69 | D |
| below 60 | F |

The boundaries are the whole exercise. 90 is an A. 89 is a B. Check both.

### 2. `parity.py`

Ask `Number: `, then print exactly `even` or `odd`. Lowercase, nothing else.

Use `%`. A number is even when dividing by 2 leaves no remainder.

### 3. `login.py`

The correct username is `admin` and the correct password is `python123`.

Ask `Username: `, then `Password: `. Print exactly one of:

```
Access granted.
Access denied.
```

Both must be right to get in. This is one `if` with an `and`, not two nested `if`s —
though write it the long way first if that is clearer to you, then shorten it.

### 4. `ticket.py`

Cinema pricing. Ask `Age: `, then `Day: `.

- Base price is **$12.00**
- Under 13 → **$8.00**
- 65 or over → **$9.00**
- Then, if the day is `Tuesday`, take **$2.00 off** whatever the price came to

Print:

```
Ticket: $10.00
```

Work out the age price first, then apply the Tuesday discount to the result. A
12-year-old on a Tuesday pays $6.00 — if your code says otherwise, your discount is in
the wrong place.

---

## Before you close the laptop

```bash
git add -A && git commit -m "day 3" && git push
```

---

## Predict-then-run

```python
age = 65
if age > 65:
    print("senior")
elif age > 18:
    print("adult")
else:
    print("minor")
```

What does a 65-year-old get? Is that what the code *meant* to say? This is an
off-by-one error, it is in production software everywhere, and it is why you check your
boundaries by hand.

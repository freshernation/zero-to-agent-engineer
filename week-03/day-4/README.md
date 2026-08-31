# Day 4 — Comprehensions, and bugs that hide inside functions

> **By the end of today** you can write a loop on one line when it earns it, and debug
> a failure that happens two function calls away from where it surfaced.

Comprehensions come last on purpose. A comprehension is a loop, compressed. Meet it
before you can write the loop and it is a magic spell; meet it after forty loops and it
is a shortcut you have earned.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on list comprehensions — 20 min]`
- [ ] `[INSTRUCTOR: source on lambda and sorted(key=) — 15 min]`

---

## What you need to know

### The shape

```python
doubled = []
for n in numbers:
    doubled.append(n * 2)
```

becomes

```python
doubled = [n * 2 for n in numbers]
```

Read it left to right: *"`n * 2`, for every `n` in `numbers`."* The thing you want
comes first, the loop that produces it comes second. That inversion is the only hard
part, and it stops being hard within a day.

### With a filter

```python
big = []
for n in numbers:
    if n > 100:
        big.append(n)
```

becomes

```python
big = [n for n in numbers if n > 100]
```

The `if` goes on the end. *"`n`, for every `n` in `numbers`, if `n` is over 100."*

### Pulling one field out of records

The one you will use most, for the rest of your life:

```python
names = [record["name"] for record in records]
totals = [r["units"] * r["price"] for r in records]
expensive = [r for r in records if r["price"] > 10]
```

### Dict comprehensions

Same idea, curly braces, and a `key: value` pair at the front:

```python
prices = {item["name"]: item["price"] for item in items}
```

### When *not* to use one

A comprehension that needs a scroll bar is worse than the loop it replaced. If you
need two conditions, a nested loop, and a calculation, write the loop — the reader
will thank you, and the reader is usually you in three weeks.

The test is simple: **can you read it in one go, out loud?** If not, it should be a loop.

### `key=` and `lambda` — now unlocked

Last week you sorted records by building `(value, name)` tuples, because this was
behind the fence:

```python
sorted(expenses, key=lambda e: e["amount"], reverse=True)
```

`lambda e: e["amount"]` is a tiny throwaway function: *"given `e`, hand back its
amount."* `sorted` calls it on every item to work out what to compare.

It is exactly what your tuple trick was doing by hand — and because you did it by hand,
you know what it costs and what it is for, rather than treating it as an incantation.
Both are fine. Use whichever reads better.

---

## Exercises

```bash
pytest week-03/day-4 -v
```

### 1. `comprehend.py`

| Function | Returns |
|---|---|
| `doubled(numbers)` | every number times two |
| `long_words(words, min_length=5)` | only the words at least `min_length` long |
| `names_only(records)` | the `"name"` of every record |
| `price_map(items)` | a **dict** of each item's `"name"` to its `"price"` |
| `top_n(records, n)` | the `n` records with the highest `"amount"`, highest first |

```python
doubled([1, 2, 3])                          # [2, 4, 6]
long_words(["hi", "hello", "hey"])          # ["hello"]
long_words(["hi", "hey"], 2)                # ["hi", "hey"]
names_only([{"name": "Ana"}])               # ["Ana"]
price_map([{"name": "Tea", "price": 2.5}])  # {"Tea": 2.5}
```

The first four must be comprehensions — there is a test that counts them. `top_n` is
the one where a comprehension is the wrong tool; use `sorted` with `key=`.

---

## Debugging, round three

Three broken files. These are harder than the last two rounds because the failure and
the cause are now in **different functions**.

| File | Should print |
|---|---|
| `broken_1.py` | `Grand total with tax: 64.80` |
| `broken_2.py` | `Counter: 3` |
| `broken_3.py` | `5.0` then `Cannot divide by zero` |

- **`broken_1.py`** crashes on a line where nothing is wrong. Read the traceback as a
  chain: the error surfaced at the bottom, the cause is further up.
- **`broken_2.py`** runs perfectly and prints the wrong number. It is the scope
  problem from Monday, and it is the most important bug of the week.
- **`broken_3.py`** has a `try` / `except` and crashes anyway. Ask why the `except`
  did not catch it.

Fill in `NOTES.md` for all three.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 3 day 4" && git push
```

Tomorrow is the milestone, and this week's defence has a phase the last two did not:
your instructor breaks one line of **your own** code and you fix it live.

---

## Predict-then-run

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("bread"))
print(add_item("milk"))
```

You would expect three baskets of one thing. You will not get that. This is the most
famous gotcha in Python and it is worth twenty minutes with the tutor — the answer is
about **when** the default value is created, and it is the same question as "where does
`total = 0` go", wearing a disguise.

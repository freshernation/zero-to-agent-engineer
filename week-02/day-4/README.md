# Day 4 — Ranking, deduplicating, and the bugs collections bring

> **By the end of today** you can put things in order, remove duplicates, and pair two
> lists together — and you can debug a loop that produces the wrong number silently.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on tuples and sets — 20 min]`
- [ ] `[INSTRUCTOR: source on sorting in Python — 15 min]`

---

## What you need to know

### Tuples — a list that cannot change

```python
point = (3, 7)
print(point[0])         # 3
point[0] = 5            # TypeError - tuples are frozen
```

Use a tuple when the thing is a fixed group that belongs together: a coordinate, a
red-green-blue colour, a `(score, name)` pair. Use a list when items get added and
removed.

### Unpacking — pulling a tuple apart

```python
point = (3, 7)
x, y = point            # x is 3, y is 7
```

You have already used this without noticing:

```python
for i, name in enumerate(names):        # enumerate hands back tuples
for key, value in contact.items():      # so does .items()
```

The number of names on the left must match the number of items on the right, or
Python complains.

### Sets — each thing once

```python
visitors = ["ana", "ben", "ana", "cara"]
unique = set(visitors)
print(unique)           # {'ana', 'ben', 'cara'}   - order is not guaranteed
print(len(unique))      # 3
```

A set is the right answer to *"how many different ones were there?"*. Because the order
is unpredictable, wrap it in `sorted()` whenever you are going to print it — otherwise
your program produces different output on different runs, which is a nightmare to test.

```python
print(sorted(set(visitors)))    # ['ana', 'ben', 'cara']   - every time
```

### `zip` — walking two lists together

```python
products = ["Widget", "Gadget"]
prices = [4.50, 12.00]

for product, price in zip(products, prices):
    print(f"{product}: ${price:.2f}")
```

`zip` pairs them up position by position. If one list is shorter, it stops at the end
of the shorter one — quietly, with no warning, which is worth remembering.

### `sorted`

```python
print(sorted([3, 1, 2]))                # [1, 2, 3]
print(sorted([3, 1, 2], reverse=True))  # [3, 2, 1]
print(sorted(["Cara", "Ana"]))          # ['Ana', 'Cara']  - alphabetical
```

`sorted()` gives you a **new** list and leaves the original alone.

### The ranking trick — the real lesson of the day

You want to sort *records* by one of their fields. The normal grown-up way needs
`key=` and a `lambda`, and both are behind the fence.

Here is what you do instead. **Tuples sort by their first item**, then their second if
the first ties:

```python
print(sorted([(3, "c"), (1, "a"), (2, "b")]))
# [(1, 'a'), (2, 'b'), (3, 'c')]
```

So: build a list of tuples with **the thing you want to sort by first**, then sort it.

```python
pairs = []
for name, score in zip(players, scores):
    pairs.append((score, name))         # score FIRST - that is the whole trick

ranked = sorted(pairs, reverse=True)    # highest score first

for score, name in ranked:
    print(name, score)
```

This is not a workaround you will throw away. Putting the sort field first is a real
technique you will still use in five years, and it makes what you are sorting by
obvious to anyone reading.

> **Worth noticing:** with `reverse=True`, tied scores come out in reverse alphabetical
> order, because the *name* breaks the tie. Nobody wants that. There is a fix, it is
> not on the fence this week, and knowing the problem exists is enough for now — but
> your instructor may well ask you about it on Friday.

---

## Exercises

```bash
pytest week-02/day-4 -v
```

### 1. `unique.py`

The file contains a `visitors` list with repeats. Print:

```
Total visits: 7
Unique visitors: 4
Names: ['ana', 'ben', 'cara', 'dev']
```

The names must come out in the same order every single run.

### 2. `pairs.py`

The file contains a `products` list and a `prices` list. Print:

```
Widget: $4.50
Gadget: $12.00
Doohickey: $3.25
```

Use `zip`. Do not loop over positions with `range(len(...))` — you have a better tool now.

### 3. `ranking.py`

The file contains a `players` list and a `scores` list. Print the top three, then two
summary lines:

```
1. Ben          892
2. Dev          733
3. Cara         615
Winner: Ben
Spread: 764
```

- Names left-aligned in 12, scores right-aligned in 4
- `Spread` is the highest score minus the lowest — the lowest, not the third

Use the tuple trick. Nothing is hard-coded: the tests run your file against a different
set of players.

---

## Debugging, round two

Three broken files. One bug each, all three about collections.

| File | Should print |
|---|---|
| `broken_1.py` | `a`, `b`, `c` on three lines |
| `broken_2.py` | `Ana 30` and `Ben 25` |
| `broken_3.py` | `Total: 20` |

`broken_3.py` runs perfectly and gives the wrong number. You saw this exact bug in
Tuesday's predict-then-run — if that is nagging at you, it should be.

Fill in `NOTES.md` for all three. Same rules as last week: your own words, and the
notes matter more than the fixes.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 2 day 4" && git push
```

Tomorrow is the milestone and your second defence.

---

## Predict-then-run

```python
print(sorted([(2, "b"), (1, "z"), (1, "a")]))
print(set([1, 2, 2, 3]) == set([3, 2, 1]))
print(list(zip([1, 2, 3], ["a", "b"])))
```

The third one loses data and does not tell you. Sit with that for a moment — it is the
kind of bug that reaches production, because nothing goes wrong until the day the two
lists stop being the same length.

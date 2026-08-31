# Day 1 — Lists

> **By the end of today** you can keep many values under one name and reach any of them.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on Python lists — 25 min]`
- [ ] `[INSTRUCTOR: source on indexing and slicing — 15 min]`

---

## What you need to know

### A list holds many values in order

```python
names = ["Ana", "Ben", "Cara"]
prices = [4.50, 7.25, 2.45]
mixed = ["Ana", 12, 4.50]        # allowed, and usually a sign you want a dict
empty = []
```

### Indexing starts at zero

This is the thing to get straight today, because everything else stands on it.

```python
names = ["Ana", "Ben", "Cara"]
print(names[0])     # Ana    <- the FIRST item is at 0
print(names[2])     # Cara
print(names[3])     # IndexError: list index out of range
```

A list of 3 items has valid positions 0, 1, 2. **The last position is always
`len(list) - 1`**, never `len(list)`. Off-by-one errors live here and they will be
with you forever, so make friends now.

Counting backwards works too, and is often clearer:

```python
print(names[-1])    # Cara   <- last
print(names[-2])    # Ben    <- second from last
```

### `len()` and `in`

```python
print(len(names))            # 3
print("Ben" in names)        # True
print("Zoe" in names)        # False
```

### Slicing — a piece of a list

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[1:4])     # [20, 30, 40]   from 1, up to but NOT including 4
print(numbers[:3])      # [10, 20, 30]   from the start
print(numbers[3:])      # [40, 50, 60]   to the end
print(numbers[::2])     # [10, 30, 50]   every second one
print(numbers[::-1])    # [60, 50, 40, 30, 20, 10]   backwards
```

**The end is not included.** `[1:4]` gives you three items, not four. This feels wrong
for about a week and then feels right forever. The reason it is designed that way:
`numbers[:3]` and `numbers[3:]` split the list perfectly with no overlap and no gap.

### Changing a list

Unlike almost everything you have met, a list can be modified after you make it:

```python
names = ["Ana", "Ben", "Cara"]

names[1] = "Bella"          # replace position 1
names.append("Dev")         # add to the end
names.insert(0, "Zoe")      # add at a position
names.remove("Cara")        # remove by value  (errors if not there)
last = names.pop()          # remove the last item AND hand it back
```

`append` is the one you will use ten times more than the rest. The pattern is always
the same: make an empty list, then add to it as you go.

```python
basket = []
basket.append("apple")
basket.append("bread")
```

---

## Exercises

```bash
pytest week-02/day-1 -v
```

### 1. `roster.py`

The file already contains this list. **Do not change it.**

```python
names = ["Ana", "Ben", "Cara", "Dev", "Eve"]
```

Print exactly five lines:

```
First: Ana
Last: Eve
Third: Cara
Count: 5
Has Ben: True
```

Get `Last` **without typing 4 or 5** — use negative indexing or `len()`. The list will
be a different length when your instructor tests it on Friday.

### 2. `slices.py`

The file already contains:

```python
numbers = [10, 20, 30, 40, 50, 60, 70, 80]
```

Print exactly four lines:

```
First three: [10, 20, 30]
Last three: [60, 70, 80]
Every other: [10, 30, 50, 70]
Backwards: [80, 70, 60, 50, 40, 30, 20, 10]
```

Printing a list directly gives you the brackets and commas for free. You do not need
to build that text yourself.

### 3. `basket.py`

Ask for three items, one at a time, with these prompts:

```
Item 1:
Item 2:
Item 3:
```

Build a list from them. Then:

- add `"bread"` to the end
- remove whatever the person typed **first**
- print the result

For a run where they type `apple`, `milk`, `eggs`:

```
Basket: ['milk', 'eggs', 'bread']
Items: 3
```

Remove the first item **by position, not by name** — you do not know what they typed.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 2 day 1" && git push
```

---

## Predict-then-run

```python
letters = ["a", "b", "c"]
print(letters[3])
print(letters[-1])
print(letters[1:1])
print(len(letters[1:99]))
```

Two of those surprise most people. The third one is the interesting one: what *is* an
empty slice, and why is it not an error when `letters[3]` is?

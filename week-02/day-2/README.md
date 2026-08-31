# Day 2 — Repetition

> **By the end of today** you can do something to every item in a collection without
> writing it out once per item.

This is the day programming starts paying for itself. Yesterday, printing ten names
meant ten `print()` lines. Today it is three lines whether there are ten names or ten
thousand.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on for loops and range — 25 min]`
- [ ] `[INSTRUCTOR: source on while loops — 15 min]`

---

## What you need to know

### `for` — do this to each item

```python
names = ["Ana", "Ben", "Cara"]

for name in names:
    print(f"Hello {name}")
```

`name` is a variable you are inventing on that line. Python fills it with the first
item, runs the indented block, fills it with the second item, runs the block again,
and so on. Call it something meaningful — `for n in names` is worse and costs nothing.

The colon and the indent work exactly like `if`. Everything indented is "inside the
loop", and that is the whole structure.

### `range` — a stretch of numbers

```python
for i in range(5):
    print(i)             # 0 1 2 3 4     <- five numbers, starting at 0

for i in range(1, 6):
    print(i)             # 1 2 3 4 5     <- stops BEFORE 6

for i in range(10, 0, -2):
    print(i)             # 10 8 6 4 2    <- start, stop, step
```

Same rule as slicing: **the stop value is not included.** `range(5)` gives you five
numbers and none of them is 5.

### The accumulator — the most important pattern this week

You want a total. You cannot add up ten numbers in one line. So you make a variable
*before* the loop and grow it *inside*:

```python
prices = [4.50, 12.00, 3.25]

total = 0                     # before the loop. Start empty.
for price in prices:
    total = total + price     # inside. Grow it.
print(total)                  # after the loop. Use it.
```

`total = total + price` reads oddly until you read it right-to-left: *work out
`total + price`, then put the answer back in `total`.* There is a shorthand:

```python
total += price      # exactly the same thing
```

**Where you put `total = 0` is the whole game.** Inside the loop, it resets every time
around and you end up with just the last item. That bug produces a plausible-looking
wrong number, no error message, and it is coming for you on Thursday.

The same shape builds a list:

```python
expensive = []
for price in prices:
    if price > 5:
        expensive.append(price)
```

### `enumerate` — when you need the position too

```python
names = ["Ana", "Ben", "Cara"]

for i, name in enumerate(names):
    print(f"{i}. {name}")        # 0. Ana / 1. Ben / 2. Cara

for i, name in enumerate(names, start=1):
    print(f"{i}. {name}")        # 1. Ana / 2. Ben / 3. Cara
```

Two variables on the left because `enumerate` hands back two things each time round.

### `while` — repeat until something changes

`for` runs once per item. `while` runs until a condition stops being true:

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

If nothing inside the loop ever makes the condition false, it runs forever. Press
<kbd>Ctrl</kbd>+<kbd>C</kbd> to stop it. You will do this today; it is not a disaster.

Use `for` when you know what you are looping over. Use `while` when you do not know how
many times — usually because you are waiting on a person.

### `break` and `continue`

```python
for n in numbers:
    if n < 0:
        continue        # skip this one, go to the next
    if n > 100:
        break           # stop the loop entirely
    print(n)
```

### The shortcuts you have now earned

```python
print(sum(prices))      # add them all up
print(len(prices))      # how many
print(max(prices))      # biggest
print(min(prices))      # smallest
```

Write the loop version first, at least once, so you know what these are doing for you.
Then use them — a `sum()` is clearer than four lines of accumulator, and clarity is
the only thing you are optimising for this year.

---

## Exercises

```bash
pytest week-02/day-2 -v
```

### 1. `countdown.py`

Print exactly:

```
10
8
6
4
2
0
Liftoff!
```

One `range()` and one loop. Do not write seven `print()` lines.

### 2. `total.py`

The file already contains:

```python
prices = [4.50, 12.00, 3.25, 7.80, 2.45]
```

Loop over it, printing each price on its own line, then a summary:

```
$4.50
$12.00
$3.25
$7.80
$2.45
---
Total: $30.00
Average: $6.00
Highest: $12.00
Lowest: $2.45
```

Build `Total` with an accumulator loop — **not** `sum()`. You can use `max()` and
`min()` for the last two. Do the average from your total and `len()`.

### 3. `numbered.py`

The file already contains:

```python
tasks = ["Write tests", "Fix the bug", "Push the branch"]
```

Print:

```
1. Write tests
2. Fix the bug
3. Push the branch
```

Numbering starts at 1, not 0.

### 4. `guess.py`

The file already contains `secret = 7`.

Ask `Guess: ` over and over until they get it. After each wrong guess print `Too low`
or `Too high`. When they are right, print how many guesses it took and stop.

A run where they type 3, then 9, then 7:

```
Too low
Too high
Correct! It took 3 guesses.
```

Count **every** guess including the right one.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 2 day 2" && git push
```

---

## Predict-then-run

```python
total = 0
for n in [1, 2, 3]:
    total = n
print(total)
```

```python
for n in [1, 2, 3]:
    total = 0
    total += n
print(total)
```

Both of those print something. Neither prints 6. Work out *why* for each, separately —
they are wrong for different reasons, and one of them is Thursday's bug.

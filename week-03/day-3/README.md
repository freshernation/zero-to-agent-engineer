# Day 3 — Remembering things

> **By the end of today** your programs survive being closed. And they can be split
> across more than one file.

Everything you have written so far forgets everything the moment it exits. Today that
changes, and with it your programs stop being exercises.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on reading and writing files — 25 min]`
- [ ] `[INSTRUCTOR: source on JSON in Python — 15 min]`

---

## What you need to know

### Opening a file

```python
with open("notes.txt", "w") as f:
    f.write("hello\n")

with open("notes.txt", "r") as f:
    contents = f.read()
```

`with` matters. It closes the file for you when the block ends, **even if something
goes wrong inside**. Without it a file can stay open, half-written, and you get data
loss that only shows up on the machine that crashed.

Two modes are enough for now:

| Mode | Does |
|---|---|
| `"r"` | read — errors with `FileNotFoundError` if it is not there |
| `"w"` | write — **creates it, or wipes it and starts over** |
| `"a"` | append — adds to the end, keeps what was there |

> `"w"` deletes everything in the file the instant you open it. Not when you write —
> when you *open*. Opening a file for writing to "check something" has destroyed a lot
> of people's data.

### Reading it back

```python
with open("notes.txt") as f:
    whole_thing = f.read()          # one big string
    
with open("notes.txt") as f:
    lines = f.readlines()           # ['hello\n', 'there\n']  - note the \n
```

`readlines()` keeps the newline on the end of every line, which is almost never what
you want. Strip it:

```python
lines = [line.rstrip("\n") for line in f.readlines()]
```

(That is a comprehension — Thursday. A plain loop is completely fine today.)

### Missing files

```python
try:
    with open(path) as f:
        contents = f.read()
except FileNotFoundError:
    contents = ""
```

A file not being there is **not an error in your program**. It is Tuesday's first day,
or a fresh install. Handle it and move on.

### JSON — saving something that is not text

A list of dicts cannot go into a text file as-is. JSON is the standard way to turn
data into text and back:

```python
import json

expenses = [{"item": "Coffee", "amount": 4.5}]

with open("data.json", "w") as f:
    json.dump(expenses, f, indent=2)        # data  -> file

with open("data.json") as f:
    expenses = json.load(f)                 # file  -> data
```

`indent=2` makes the file readable by a human, which you will want the first time
something is wrong with it.

JSON handles lists, dicts, strings, numbers, booleans and `None`. It does not handle
tuples (they come back as lists) or anything more exotic.

You will meet JSON constantly from week 5 — it is what every web API on earth speaks.

### Two ways a saved file betrays you

```python
try:
    with open(path) as f:
        return json.load(f)
except FileNotFoundError:
    return default              # first run - fine
except json.JSONDecodeError:
    return default              # the file exists but is damaged
```

The second one is the interesting case. A file half-written when the power went out,
or edited by hand and left with a trailing comma. A program that handles the missing
file but not the corrupt one works perfectly until the day it does not.

### Splitting into several files

A file of your own functions is a **module**, and another file can use it:

```python
# store.py
def save_data(path, data):
    ...

# app.py
import store
store.save_data("out.json", stuff)

# or
from store import save_data
save_data("out.json", stuff)
```

Both work. `import store` keeps it obvious where `save_data` came from; `from store
import save_data` is shorter. Pick one per project and be consistent.

### `if __name__ == "__main__":`

Here is the problem it solves. **Everything in a file runs when you import it.** So if
`app.py` has a `print()` at the bottom, importing `app` prints. If it has an `input()`,
importing it stops and waits for a person who is not there.

```python
def record_visit(path):
    ...

if __name__ == "__main__":
    print(record_visit("visits.json"))
```

`__name__` is a variable Python sets for you. It is `"__main__"` when the file is being
**run**, and the module's own name when it is being **imported**. So the guarded block
runs on `python3 app.py` and is skipped by `import app`.

**Every file that both defines things and does things needs this.** It is the line that
lets one file be a library and a program at the same time, and today's tests check for it.

---

## Exercises

```bash
pytest week-03/day-3 -v
```

The tests hand your functions a path to a temporary file, so nothing you write today
lands in your repo.

### 1. `notes.py` — plain text

| Function | Does |
|---|---|
| `save_lines(path, lines)` | writes each item on its own line, replacing the file |
| `load_lines(path)` | returns a list of lines with no newline characters, or `[]` if the file does not exist |
| `append_line(path, line)` | adds one line at the end, keeping what was there |

```python
save_lines("/tmp/a.txt", ["one", "two"])
load_lines("/tmp/a.txt")            # ["one", "two"]
append_line("/tmp/a.txt", "three")
load_lines("/tmp/a.txt")            # ["one", "two", "three"]
load_lines("/tmp/nothing.txt")      # []
```

### 2. `store.py` — JSON

| Function | Does |
|---|---|
| `save_data(path, data)` | writes `data` as JSON |
| `load_data(path, default=None)` | reads it back, or returns `default` if the file is **missing or damaged** |

```python
save_data(p, {"a": 1})
load_data(p)                        # {"a": 1}
load_data("/tmp/nope.json")         # None
load_data("/tmp/nope.json", [])     # []
# and if the file contains "{not json" -> the default, not a crash
```

### 3. `app.py` — two files working together

`app.py` uses `store.py`. It must define:

**`record_visit(path)`** — load the number from `path` (0 if there is nothing there),
add one, save it back, and **return** the new number.

Then, guarded by `if __name__ == "__main__":`, print:

```
Visits: 1
```

Run it again and it says `Visits: 2`.

The tests import `app.py` and check that **nothing is printed** on import, then run it
as a program and check that it does. Get the guard wrong and you will fail one of those
two, which is exactly what it is there to catch.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 3 day 3" && git push
```

Read the milestone spec tonight — it is this, with a menu on top.

---

## Predict-then-run

Make a file `t.txt` with three lines in it. Then:

```python
with open("t.txt", "w") as f:
    pass
print(open("t.txt").read())
```

That block does not write a single thing. Explain why the file is now empty anyway.
It is the most expensive lesson on this page.

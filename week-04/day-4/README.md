# Day 4 — Types, documentation, and bugs that classes bring

> **By the end of today** your code says what it expects, and you can debug the three
> failures that only happen once you have objects.

---

## Read / watch first

- [ ] [**Python type hints**](../../content/week-04/day-4/type-hints.md) — 20 min · docs: [`typing`](https://docs.python.org/3.14/library/typing.html)
- [ ] [**Writing a good README**](../../content/week-04/day-4/writing-a-good-readme.md) — 15 min · docs: [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

---

## What you need to know

### Type hints

```python
def split_bill(total: float, people: int) -> float:
    return round(total / people, 2)
```

`: float` says what goes in. `-> float` says what comes back.

**Python ignores them completely at runtime.** Nothing is checked, and passing a string
still works exactly as badly as before. So why write them?

- Your editor can now autocomplete and warn you before you run anything
- `-> float` documents the promise a docstring makes in prose
- On a real team, a tool checks them and catches whole classes of bug before merge

The common ones:

```python
name: str
count: int
price: float
active: bool
items: list
lookup: dict
nothing: None
```

For "a string, or nothing at all":

```python
from typing import Optional

def find_user(name: str) -> Optional[str]:
    ...
```

`Optional[str]` means *"a `str` or `None`"*, and writing it forces you to notice that
your function can return nothing — which is exactly the case people forget to handle.

Methods get them too, and `self` never does:

```python
class Task:
    def __init__(self, title: str, done: bool = False) -> None:
        self.title = title
        self.done = done

    def complete(self) -> None:
        self.done = True
```

`__init__` returns `None` — it sets things up, it does not hand anything back.

### READMEs

Tomorrow you publish a repository. The README is the only thing most people will ever
read, and a project without one reads as unfinished no matter how good the code is.

The five sections that matter, in this order:

1. **What it is** — one sentence, no throat-clearing
2. **What it does** — three or four bullets, features not implementation
3. **How to run it** — commands they can paste, that actually work
4. **How to run the tests** — the line that says this is real
5. **What you would do next** — honest, brief, and the section interviewers notice

Write it for someone who has never seen the project and has four minutes.

---

## Exercises

```bash
pytest week-04/day-4 -v
```

### 1. `typed.py`

Every function and method must carry type hints.

| Thing | Signature |
|---|---|
| `total(prices)` | takes a `list`, returns a `float` — the sum, rounded to 2dp |
| `label(name, amount)` | `str`, `float` → `str` — `"Coffee: $4.50"` |
| `find(names, target)` | `list`, `str` → `int` — the position, or `-1` if it is not there |
| `first_match(names, letter)` | `list`, `str` → `Optional[str]` — the first name starting with `letter`, or `None` |
| `Task(title, done=False)` | `str`, `bool` → `None` |
| `Task.complete()` | → `None` — marks it done |
| `Task.summary()` | → `str` — `"[x] Write tests"` when done, `"[ ] Write tests"` when not |

The tests check both that the behaviour is right **and** that the annotations are there.

---

## Debugging, round four

Three broken files. All three are bugs you can only have once you have classes.

| File | Should print |
|---|---|
| `broken_1.py` | `Area: 12` |
| `broken_2.py` | `Ana: ['apple']` then `Ben: []` |
| `broken_3.py` | `Total: 30` |

- **`broken_1.py`** has a confusing `TypeError`. The argument counts do not seem to
  add up — remember what `r.area()` is shorthand for.
- **`broken_2.py`** runs fine and gives two people the same shopping. You met this in
  Tuesday's predict-then-run.
- **`broken_3.py`** runs fine and the total stays at zero. You met *this* one in week
  3, in a function. It looks different in a class and it is the same bug.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 4 day 4" && git push
```

Tomorrow: Project 1, the defence, and your first mock interview.

---

## Predict-then-run

```python
class Basket:
    def __init__(self, items: list = []) -> None:
        self.items = items

    def add(self, item: str) -> None:
        self.items.append(item)

a = Basket()
b = Basket()
a.add("apple")
print(b.items)
```

Fully type-hinted, and still wrong. This is the same trap as `broken_2.py` wearing a
different disguise, and it is the strongest argument you will ever meet for why type
hints are documentation rather than safety.

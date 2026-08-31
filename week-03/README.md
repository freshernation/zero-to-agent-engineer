# Week 3 — Pieces, storage, and failure

> **Destination**
> Break a program into named pieces, save its state to disk, and handle things going
> wrong on purpose instead of by accident.

Your programs so far have been one file, run once, forgotten. This week they gain the
three properties that separate a script from software: they are **made of parts**, they
**remember things**, and they **survive bad input**.

This is the last week of Python-only. Everything from week 5 onwards — API responses,
model calls, agent state, retrieval results — is built out of what you learn in the
next two weeks.

Still **AI-off for writing code**.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Package logic into functions that hand answers back |
| Tue | `day-2/` | Catch failures on purpose and raise your own |
| Wed | `day-3/` | Save data to disk and read it back, across several files |
| Thu | `day-4/` | Write comprehensions, and debug across function calls |
| Fri | `milestone/` | Ship the expense tracker, then defend it |

---

## The one idea this week is really about

**A function is a promise: give me these inputs, I will hand you back this answer.**

Everything else — scope, `return`, exceptions, modules — falls out of taking that
promise seriously. A function that prints instead of returning has broken the promise.
A function that crashes on bad input has broken it. A function that quietly changes
something outside itself has broken it in the way that is hardest to find.

Hold onto that sentence when Thursday's bugs stop making sense.

---

## What changes about the tests

Until now the tests ran your file and read what it printed. From this week they
**import your file and call your functions directly**:

```python
money = load("money.py")
assert money.add_tax(100) == 108.00
```

Two consequences, and they will both bite you today rather than later:

1. **Your function must `return`, not `print`.** A printed answer is invisible to
   anyone calling your code. This is the single most common week-3 mistake.
2. **Files that only define functions must not do anything when imported.** No
   top-level `input()`, no code that runs on its own. Wednesday gives you the
   `if __name__ == "__main__":` guard for exactly this.

---

## Milestone

A two-file expense tracker that saves to JSON, survives a corrupted save file, and
cannot be crashed by anything a person types. Spec in `milestone/README.md`.

It is the first thing you will build that is recognisably a **program** rather than an
exercise, and the first one worth putting in front of someone.

# Week 1 — Concept fence

Every AI role in `ai/` reads this. Paste the two lists into the role prompt before you
start a session, so the model teaches you with the toolkit you actually have.

## Allowed

- Running a file: `python3 filename.py`
- `print()` — one or many values, `sep=`, `end=`
- Comments with `#`
- Variables and assignment
- Types: `str`, `int`, `float`, `bool`
- Conversion: `int()`, `float()`, `str()`
- `input()` and the fact that it always gives you a `str`
- f-strings, including `f"{value:.2f}"` for decimal places
- Arithmetic: `+ - * / // % **`, and parentheses for order
- Comparison: `== != < > <= >=`
- Boolean logic: `and`, `or`, `not`
- `if` / `elif` / `else`, including nesting
- Reading a traceback
- git: `add`, `commit`, `push`

## Not yet

Lists · dicts · tuples · sets · `for` · `while` · `range` · functions and `def` ·
`import` and any library · `try` / `except` · file reading and writing · classes ·
comprehensions · `lambda` · `match` · slicing · string methods beyond none at all ·
ternary expressions

---

## Why the fence exists

Every task this week is solvable with the "allowed" list. They were designed that way.

If an AI answers your week-1 question with a list comprehension, it has not made you
faster — it has taught you that the tools you own are inadequate, three days into
learning them. That feeling is the most common reason beginners quit, and it is
entirely manufactured.

Solving a problem with a small toolkit is not a limitation. It is the entire skill.

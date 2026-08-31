# Week 3 — Concept fence

Paste both lists into any AI role before you start a session.

## Allowed

**Everything from Weeks 1 and 2**, plus:

- **Functions** — `def`, parameters, `return`, calling one function from another,
  default arguments, keyword arguments, docstrings
- **Scope** — local variables, why a function cannot change a variable outside itself
  by assigning to it
- **Errors** — `try` / `except` / `else` / `finally`, catching a *specific* exception
  type, `raise ValueError("message")`, reading a traceback across several functions
- **Files** — `with open(path) as f:`, `.read()`, `.write()`, `.readlines()`, modes
  `"r"` and `"w"`
- **JSON** — `import json`, `json.dump()`, `json.load()`, `json.JSONDecodeError`
- **Your own modules** — `import mymodule`, `from mymodule import thing`,
  `if __name__ == "__main__":`
- **Comprehensions** — `[x for x in things]`, with an `if` filter, and the dict form
- **`key=`** — now unlocked, with a named function *or* a `lambda`
- `sorted()`, `sum()`, `max()`, `min()`, `enumerate()`, `zip()`, `round()`, `abs()`
- `os.path.exists()` and `pathlib.Path` if you want them (not required anywhere)

## Not yet

Decorators · `*args` / `**kwargs` · writing your own context managers · custom
exception classes · `logging` · generators and `yield` · classes and `self` ·
type hints · `dataclasses` · testing frameworks · `itertools` · `collections` ·
regular expressions · any third-party library

---

## Two things unlocked this week

**`key=` and `lambda`.** Last week you sorted records by building `(value, name)`
tuples, because `key=` was behind the fence. It is open now:

```python
sorted(expenses, key=lambda e: e["amount"], reverse=True)
```

Do not throw the tuple trick away — it is still the clearer choice sometimes, and you
now understand what `key=` is doing because you did it by hand.

**Comprehensions.** These arrive last, on Thursday, on purpose. A comprehension is a
loop written on one line, and if you meet it before you can write the loop, it is a
magic incantation rather than a shortcut. You have written the loop forty times now.

# Week 2 — Concept fence

Paste both lists into any AI role before you start a session.

## Allowed

**Everything from Week 1**, plus:

- **Lists** — creating, indexing, negative indexing, `len()`, slicing `[a:b:step]`,
  `in`, `append()`, `insert()`, `remove()`, `pop()`, changing an item in place
- **Tuples** — creating, unpacking (`price, name = pair`), the fact that they cannot
  be changed, and that they sort by their first item
- **Sets** — creating with `set()`, uniqueness, `in`
- **Dicts** — creating, `d["key"]`, adding and updating, `in` for keys,
  `.keys()`, `.values()`, `.items()`, `.get()` with a default
- **Nested structures** — lists of dicts, dicts of lists
- **Loops** — `for x in thing:`, `range(a, b, step)`, `enumerate()`, `zip()`,
  `while`, `break`, `continue`
- **Builtins** — `sum()`, `max()`, `min()`, `sorted()`, `reversed()`, `round()`
- **f-string alignment** — `{name:<12}`, `{n:>3}`, `{title:^20}`

## Not yet

`def` and functions · `lambda` · **the `key=` argument to `sorted()` / `max()` / `min()`** ·
`.sort()` (use `sorted()` for now) · comprehensions · `import` and any library ·
`try` / `except` · file reading and writing · classes · generators · `itertools` ·
`collections` · string methods · recursion

---

## The one that will bite

**`key=` is fenced off on purpose.** Sorting a list of dicts by one of their fields is
the natural thing to reach for this week, and the normal way to do it —
`sorted(records, key=lambda r: r["revenue"])` — needs two things you have not met.

There is a way to do it with what you have, and finding it is one of the real lessons
of the week. The hint, and it is the only one you get: **tuples sort by their first
item.** Build the right list of tuples and `sorted()` needs no help at all.

If an AI hands you a `lambda` this week, it has skipped the lesson. Ask it to solve the
problem inside the fence instead.

# Day 4 — Reading failure

> **By the end of today** you can look at a traceback, say what went wrong and where,
> and fix code you did not write.

Today there are no new concepts. Today is about the skill nobody teaches and every
interview tests: **being handed broken code and staying calm.**

Here is the thing worth internalising early. Professional programmers do not write code
that works. They write code that is broken, read the error, and fix it — dozens of times
an hour, for their whole career. The error message is not a punishment or a sign you are
not cut out for this. It is the most useful output your program produces.

---

## Read / watch first

- [ ] [**Reading Python tracebacks**](../../content/week-01/day-4/reading-python-tracebacks.md) — 20 min · docs: [Errors and Exceptions](https://docs.python.org/3.14/tutorial/errors.html)

---

## How to read a traceback

```
Traceback (most recent call last):
  File "/Users/sam/code/broken_3.py", line 2, in <module>
    print("You are " + age + " years old.")
                       ~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

**Read it from the bottom up.** Always.

| Line | What it tells you |
|---|---|
| **Last line** | *What* went wrong: `TypeError`, and the explanation |
| **Line above** | *Which line of your code*: line 2, and the code itself |
| **The `^^^^` marks** | *Which part* of that line |
| Everything above | How Python got there. Ignore it for now. |

The top of a traceback is the least useful part, which is unfortunate, because it is
the part beginners read.

## The five errors you will meet today

| Error | Usually means |
|---|---|
| `SyntaxError` | Python could not even read your file. A missing bracket, quote, or colon — often on the line *before* the one it points at. |
| `IndentationError` | Your spacing does not match your structure. |
| `NameError` | You used a name Python has never seen. Almost always a typo, or using something before you created it. |
| `TypeError` | You did something to a value its type does not support. Adding text to a number is the classic. |
| `ValueError` | The type was right but the value was not. `int("hello")` — it *is* text, it is just not a number. |

And the sixth, which has no error message at all:

| **A logic bug** | It runs. It finishes. It gives the wrong answer. This is the dangerous one, and the only defence is knowing what the right answer should have been. |

## The method

When something breaks, do these in order. Do not skip to guessing.

1. **Read the last line of the traceback.** Out loud if you are alone.
2. **Go to the line number it names.** Look at that line only.
3. **Say what you expected that line to do**, in words.
4. **Print the values.** `print(age)`, `print(type(age))`. Do not reason about what a
   variable contains — go and look.
5. **Change one thing.** Run it. If it did not help, change it back.

Step 5 is the discipline that separates debugging from thrashing. Changing three things
at once and getting a different error teaches you nothing about which change did what.

---

## Exercises

There are five broken files in this folder. Each has exactly **one** bug, and each bug
is a different kind. Fix them in place — you may only change what needs changing.

```bash
pytest week-01/day-4 -v
```

Before you fix each one:

- Run it. `python3 broken_1.py`
- Read the error out loud.
- **Predict the fix before you make it.**

| File | Should print |
|---|---|
| `broken_1.py` | `Hello, Sam` |
| `broken_2.py` | `Average: 8.0` |
| `broken_3.py` | `You are 30 years old.` |
| `broken_4.py` | `Pass` |
| `broken_5.py` | `Area: 21` |

`broken_5.py` runs perfectly and prints the wrong number. There is no traceback to help
you. Work out what the answer *should* be first, then find where the code disagrees.

---

## `NOTES.md` — the actual deliverable

Open `NOTES.md` and fill in all five entries. This is graded, and it matters more than
the fixes.

Anyone can fix five bugs by trying things. Writing down what the error meant is what
turns today into a skill you still have in week 12 — and "tell me about a bug you
found and how you found it" is a real interview question you will get asked.

---

## Before you close the laptop

```bash
git add -A && git commit -m "day 4" && git push
```

Tomorrow is the milestone and your first defence. Read
`week-01/milestone/README.md` tonight so it is not new in the morning.

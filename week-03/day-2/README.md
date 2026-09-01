# Day 2 — Failing on purpose

> **By the end of today** you can stop a program from crashing on bad input, and raise
> your own errors when the input is wrong in a way only you can judge.

In week 1 an error meant you had written something wrong. From today an error is also a
**tool** — something you catch when you can recover, and something you throw when you
cannot.

---

## Read / watch first

- [ ] [**`try` / `except`**](../../content/week-03/day-2/try-except.md) — 25 min · docs: [Handling Exceptions](https://docs.python.org/3.14/tutorial/errors.html#handling-exceptions)
- [ ] [**Raising exceptions**](../../content/week-03/day-2/raising-exceptions.md) — 15 min · docs: [Raising Exceptions](https://docs.python.org/3.14/tutorial/errors.html#raising-exceptions)

---

## What you need to know

### `try` / `except`

```python
try:
    age = int(input("Age: "))
except ValueError:
    age = 0
```

*Try this. If it blows up with a `ValueError`, do that instead.* The program keeps
running either way.

### Catch the specific one

```python
except ValueError:          # good - you know what you are recovering from
except:                     # bad  - catches everything, including your own typos
except Exception:           # nearly as bad
```

A bare `except:` swallows every error in the block, including the `NameError` from a
misspelt variable. Your program then does the wrong thing *silently*, which is far
worse than crashing. **Name the exception you expect.** If you cannot name it, you do
not yet know what you are recovering from.

You will meet code online full of bare `except:`. It is one of the clearest signals
that the person writing it did not know what could go wrong.

### The error object

```python
try:
    amount = float(text)
except ValueError as error:
    print(f"Could not read that: {error}")
```

`as error` gives you the exception itself, and printing it tells you what Python
actually objected to.

### `else` and `finally`

```python
try:
    value = int(text)
except ValueError:
    print("Not a number")
else:
    print(f"Got {value}")     # runs only if NOTHING went wrong
finally:
    print("Done")             # runs either way, always
```

`else` keeps the `try` block down to the one line that might fail, which makes it
obvious what you are guarding. `finally` is for cleanup that must happen whatever
occurred.

### Raising your own

Catching is half of it. The other half is refusing bad input yourself:

```python
def parse_age(text):
    """Return the age as a whole number, or raise ValueError."""
    age = int(text)                     # raises ValueError on its own if text is junk
    if age < 0 or age > 130:
        raise ValueError("Age must be between 0 and 130")
    return age
```

`int("abc")` already raises `ValueError`. But `int("200")` works fine — 200 is a
perfectly good number and a terrible age. Only your function knows that, so your
function is what has to say so.

**Put a real message in it.** `raise ValueError("Age must be between 0 and 130")` tells
whoever hits it what to do. `raise ValueError("bad input")` tells them nothing and will
one day waste an hour of your own life.

### Which exception is which

| Exception | Raised when |
|---|---|
| `ValueError` | Right type, wrong value — `int("abc")`, a negative price |
| `TypeError` | Wrong type entirely — `"5" + 5`, calling `None` |
| `KeyError` | A dict key that is not there |
| `IndexError` | A list position that is not there |
| `ZeroDivisionError` | Dividing by zero |
| `FileNotFoundError` | Opening a file that does not exist (tomorrow) |

`ValueError` is the one you will raise yourself nine times out of ten.

### Tracebacks now have layers

This is what changes today. Your functions call other functions, so a traceback has
several frames:

```
Traceback (most recent call last):
  File "app.py", line 12, in <module>
    show_report(records)
  File "app.py", line 8, in show_report
    total = add_all(records)
  File "app.py", line 4, in add_all
    return sum(r["amount"] for r in records)
KeyError: 'amount'
```

Still read it bottom-up: the **last line** is what went wrong, and the frame just above
it is where. But now there is a second question worth asking:

> **Which of these frames is code I wrote?**

The bottom frame is where the error surfaced. The bug is often one frame **up** — in
whoever passed in the bad value. Here, `add_all` is innocent; it was handed records
without an `amount` key, and the real bug is wherever those records were built.

Reading a traceback as a *chain of blame* rather than a single line is the skill that
separates a week-3 student from a week-1 one.

---

## Exercises

```bash
pytest week-03/day-2 -v
```

### 1. `safe.py` — functions that never crash

| Function | Returns |
|---|---|
| `to_int(text, default=0)` | `text` as a whole number, or `default` if it cannot be |
| `to_float(text, default=0.0)` | same, as a decimal |
| `safe_divide(a, b)` | `a / b`, or `None` if `b` is zero |

```python
to_int("42")            # 42
to_int("abc")           # 0
to_int("abc", -1)       # -1
to_float("4.5")         # 4.5
safe_divide(10, 2)      # 5.0
safe_divide(10, 0)      # None
```

Catch the **specific** exception in each. There is a test that fails you for a bare
`except:`.

### 2. `validate.py` — functions that refuse bad input

| Function | Returns / raises |
|---|---|
| `parse_age(text)` | the age as an `int`, or raises `ValueError` |
| `parse_amount(text)` | the amount as a `float`, or raises `ValueError` |

The exact messages matter — they get shown to a person:

| Input | Message |
|---|---|
| `parse_age("abc")` | `Age must be a whole number` |
| `parse_age("-5")` | `Age must be between 0 and 130` |
| `parse_age("200")` | `Age must be between 0 and 130` |
| `parse_amount("abc")` | `Amount must be a number` |
| `parse_amount("-3")` | `Amount cannot be negative` |

`parse_age("30")` returns `30`. `parse_amount("4.50")` returns `4.5`. Note that
`parse_age` has to turn Python's own unhelpful `ValueError` into your readable one.

### 3. `ask.py` — a script that will not give up

This one is a program, not a library: it has top-level code and the tests run it.

Ask `Age: ` over and over until the person gives a valid one. Print the problem and
ask again each time. A run where they type `abc`, then `200`, then `30`:

```
That is not a number. Try again.
Age must be between 0 and 130. Try again.
Thanks, you are 30.
```

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 3 day 2" && git push
```

---

## Predict-then-run

```python
def get_price(prices, item):
    try:
        return prices[item]
    except:
        return 0

prices = {"apple": 1.50}
print(get_price(prices, "pear"))
print(get_price(prices, "aple"))
print(get_prices(prices, "apple"))
```

The first two return 0 and look fine. The third is a typo in the *function name*.
Now change the bare `except:` to `except KeyError:` and run it again — the same three
lines behave differently, and one of them starts telling you the truth.

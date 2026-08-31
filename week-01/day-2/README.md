# Day 2 — Values that vary

> **By the end of today** you can store a value, do arithmetic on it, read what a
> person types, and format the result to look like money.

Yesterday your programs printed the same thing every time. Today they start reacting.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on variables and types — 25 min]`
- [ ] `[INSTRUCTOR: source on input() and type conversion — 20 min]`

---

## What you need to know

### Variables

A variable is a name pointing at a value. `=` does not mean "equals" — it means
*"put the thing on the right into the name on the left"*.

```python
price = 4.50
price = price + 1     # perfectly normal. Read it right-to-left.
```

Names matter more than you think. `p` and `x` and `temp` are how you make code you
cannot read in a week. Spell it out: `price`, `people_count`, `tip_rate`.

### The four types you meet today

```python
name  = "Sam"     # str   - text, always in quotes
count = 4         # int   - whole number
price = 4.50      # float - number with a decimal point
is_ok = True      # bool  - True or False, capitalised
```

Ask Python if you are unsure: `print(type(price))`.

### `input()` always gives you text

This is the single biggest trap of the week:

```python
age = input("Age: ")
print(age + 1)          # TypeError!
```

`input()` **always** returns a `str`, even when the person typed digits. `"30" + 1` is
meaningless, so Python refuses. You have to convert:

```python
age = int(input("Age: "))       # now it is a number
bill = float(input("Bill: "))   # use float when decimals are possible
```

`int()` for whole numbers, `float()` for anything that can have a decimal point.

### Arithmetic

| | | |
|---|---|---|
| `+` `-` `*` | as expected | |
| `/` | division, **always gives a float** | `7 / 2` → `3.5` |
| `//` | floor division, throws away the remainder | `7 // 2` → `3` |
| `%` | remainder | `7 % 2` → `1` |
| `**` | power | `2 ** 3` → `8` |

Parentheses work exactly like in maths, and you should use them even when you do not
need to. `(a + b) / 2` is kinder than `a + b / 2` is wrong.

### f-strings

Put an `f` before the quotes and you can drop values straight into text:

```python
name = "Sam"
total = 27.5
print(f"Hello {name}, you owe {total}")      # Hello Sam, you owe 27.5
```

Money needs two decimal places, always. Add `:.2f` inside the braces:

```python
print(f"Total: ${total:.2f}")      # Total: $27.50
print(f"Total: ${total}")          # Total: $27.5     <- looks broken, is broken
```

`:.2f` means *"as a decimal number, two places"*. `:.1f` gives one place. This is how
every number you print for a human should be formatted.

---

## Exercises

```bash
pytest week-01/day-2 -v
```

Use the **exact** prompt text given. The tests type answers into your program in the
order the task lists, so the order of your `input()` calls matters.

### 1. `greet.py`

Ask `Name: `, then print:

```
Hello, Sam! Welcome to Python.
```

(with whatever they typed in place of Sam)

### 2. `age.py`

The current year is **2026** — store it in a variable rather than burying `2026` in
the middle of a calculation.

Ask `Birth year: `, then print:

```
You are 36 years old.
```

### 3. `convert.py`

Ask `Celsius: `, convert to Fahrenheit, then print, **both to one decimal place**:

```
37.0C = 98.6F
```

The formula is `F = C * 9 / 5 + 32`. Watch your parentheses.

### 4. `checkout.py`

Tax is **8%** — store the rate in a variable.

Ask `Price: `, then `Quantity: `, then print three lines:

```
Subtotal: $25.00
Tax: $2.00
Total: $27.00
```

Subtotal is price times quantity. Tax is 8% of the subtotal. Total is both added.
All money to two decimal places.

---

## Before you close the laptop

```bash
git add -A && git commit -m "day 2" && git push
```

Log your stuck events and your five numbers.

---

## Predict-then-run

```python
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(int("7") + 1)
print("7" + "1")
print(0.1 + 0.2)
```

That last one is not a bug in Python and not a bug in your computer. Ask the tutor
why — it is a good twenty minutes, and it is the reason money is always printed
with `:.2f`.

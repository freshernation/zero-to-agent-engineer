# Day 1 — Make the machine do something

> **By the end of today** you can write a file, run it, and make it print exactly what
> you meant — including the awkward characters.

Today's real lesson is not `print()`. It is this: **the computer does exactly what you
say, and nothing else.** Every bug you hit for the rest of your life is a version of
that sentence. Today you meet it for the first time, on purpose, in a safe place.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on running Python + print — 20-30 min]`
- [ ] `[INSTRUCTOR: source on strings and quotes — 15 min]`

---

## What you need to know

### Running a file

Make a file ending in `.py`. Put code in it. Run it:

```bash
python3 hello.py
```

That is the whole loop. Edit, save, run, look. You will do it ten thousand times.

### `print()`

```python
print("Hello")            # Hello
print("a", "b")           # a b        <- print puts a space between values
print("a", "b", sep="")   # ab
print(3 + 4)              # 7          <- no quotes: this is a calculation
print("3 + 4")            # 3 + 4      <- quotes: this is just text
```

The difference between those last two lines is the difference between a number and a
picture of a number. Sit with that for a second; it comes back all week.

### Comments

```python
# Anything after a hash is for humans. Python ignores it.
print("this runs")  # this bit does not
```

### Quotes inside quotes

This is broken — Python thinks the string ended at the second `"`:

```python
print("She said "hello" and left.")     # SyntaxError
```

Two ways to fix it. Either use different quotes on the outside:

```python
print('She said "hello" and left.')
```

or **escape** the inner ones with a backslash, which means *"this next character is
text, not punctuation"*:

```python
print("She said \"hello\" and left.")
```

### Escape sequences

A backslash starts a special instruction inside a string:

| You type | You get |
|---|---|
| `\n` | a new line |
| `\t` | a tab |
| `\"` | a literal `"` |
| `\\` | a literal `\` |

Which leads to the trap that catches everybody:

```python
print("C:\Users\new")
```

That does not print a Windows path. `\U` and `\n` are instructions, so you get a
mangled line and a newline in the middle. To print an actual backslash you need two:

```python
print("C:\\Users\\new")     # C:\Users\new
```

---

## Exercises

Do them in order. Run the tests after each one.

```bash
pytest week-01/day-1 -v
```

### 1. `hello.py`

Print exactly three lines:

1. `Hello, world!` — exactly that, capital H, the comma, the exclamation mark
2. Your name
3. One line on why you are doing this course

Line 1 is checked exactly. Lines 2 and 3 just have to exist and not be empty. Write
something true on line 3; you will read it again in week 8 when it is hard.

### 2. `receipt.py`

Print this receipt, exactly. Every character.

```
=========================
     THE CORNER CAFE
=========================
Flat white           3.40
Croissant            2.75
-------------------------
TOTAL                6.15
=========================
```

The banner lines are 25 characters wide. The prices end at column 25. Count them.
You do not need any clever technique — just spaces inside strings.

> This exercise is tedious on purpose. Precision is the job. A program that is *almost*
> right is wrong, and the sooner that stops feeling unfair the better.

### 3. `escapes.py`

Print exactly these three lines:

```
She said "hello" and left.
Path: C:\Users\new
Name	Score
```

Line 3 has a **tab** between `Name` and `Score`, not spaces.

Every one of these lines needs an escape sequence or a quote choice. Get all three with
**three** `print()` calls.

---

## Before you close the laptop

```bash
git add -A
git commit -m "day 1"
git push
```

Then fill in `logs/signal-log.md`. Two minutes.

---

## Predict-then-run

Do this before you run anything today. Write your prediction down, then run it, then
note whether you were right.

```python
print("2" + "2")
print(2 + 2)
print("2" * 3)
print(2 * 3)
```

If any of those four surprised you, that surprise is the most valuable thing that
happened today. Bring it to the live hour.

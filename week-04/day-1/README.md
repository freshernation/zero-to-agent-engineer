# Day 1 — Classes

> **By the end of today** you can bundle data together with the behaviour that acts
> on it.

---

## Read / watch first

- [ ] [**Python classes and `__init__`**](../../content/week-04/day-1/classes-and-init.md) — 30 min · docs: [Classes](https://docs.python.org/3.14/tutorial/classes.html)
- [ ] [**`self` and instance attributes**](../../content/week-04/day-1/self-and-instance-attributes.md) — 15 min · docs: [Class and Instance Variables](https://docs.python.org/3.14/tutorial/classes.html#class-and-instance-variables)

---

## What you need to know

### The problem classes solve

Last week an expense was a dict, and the functions that worked on it were somewhere
else:

```python
expense = {"description": "Coffee", "amount": 4.5}
print(format_expense(expense))
```

Nothing stops someone building a dict with a missing key, or a `format_expense` that
gets handed a dict of something else entirely. The data and the rules about it have
drifted apart.

A class keeps them together:

```python
class Expense:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    def label(self):
        return f"{self.description}: ${self.amount:.2f}"
```

```python
coffee = Expense("Coffee", 4.5)
print(coffee.amount)        # 4.5
print(coffee.label())       # Coffee: $4.50
```

### The vocabulary

- `class Expense:` — a **class** is the blueprint
- `Expense("Coffee", 4.5)` — calling it makes an **instance**
- `__init__` — runs automatically when the instance is made. Set your attributes here.
- `self` — the instance the method was called on
- `self.amount` — an **attribute**, belonging to this one instance
- `def label(self)` — a **method**: a function that lives on the class

### `self` is not magic

`coffee.label()` is Python's shorthand for `Expense.label(coffee)`. The instance is
passed in as the first argument, and by convention it is called `self`. That is the
whole story.

Two rules follow from it, and they cover most first-day errors:

1. **Every method takes `self` first.** Forget it and you get
   `TypeError: label() takes 0 positional arguments but 1 was given` — which is
   confusing until you know that `coffee` was the one argument.
2. **Inside a method, reach for your own data through `self`.** Plain `amount` is a
   local variable; `self.amount` is the instance's.

### Methods that change the instance

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
```

`deposit` returns nothing — it changes the object. That is the one honest exception to
week 3's "take values in, hand new ones back": **a method may change its own instance,
because that is what the object is for.** Changing anything else is still a bug.

### Methods that refuse

```python
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

An object that can enforce its own rules is most of why classes exist. A dict cannot
stop you setting a negative balance. This can.

---

## Exercises

```bash
pytest week-04/day-1 -v
```

### 1. `rectangle.py`

`Rectangle(width, height)` with attributes `width` and `height`, and:

| Method | Returns |
|---|---|
| `area()` | width times height |
| `perimeter()` | twice the width plus twice the height |
| `is_square()` | `True` if width equals height |
| `scale(factor)` | nothing — multiplies both sides by `factor` |

```python
r = Rectangle(3, 4)
r.area()            # 12
r.is_square()       # False
r.scale(2)
r.width             # 6
r.area()            # 48
```

### 2. `account.py`

`BankAccount(owner, balance=0)` with attributes `owner` and `balance`, and:

| Method | Does |
|---|---|
| `deposit(amount)` | adds to the balance; raises `ValueError("Deposit must be positive")` for zero or less |
| `withdraw(amount)` | subtracts; raises `ValueError("Insufficient funds")` if there is not enough |
| `can_afford(amount)` | returns `True` or `False`, changes nothing |

A failed deposit or withdrawal must leave the balance **exactly as it was**. There is a
test for that — an object that half-applies a change is worse than one that refuses.

### 3. `inventory.py`

`Inventory()` — starts empty, with:

| Method | Does |
|---|---|
| `add(name, quantity)` | adds that many; adds to the count if the name is already there |
| `remove(name, quantity)` | takes that many away; raises `ValueError("Not enough Widget")` naming the item |
| `quantity_of(name)` | how many, `0` if never seen |
| `total_items()` | every quantity added together |
| `is_empty()` | `True` when there is nothing with a quantity above zero |

Store it however you like inside — a dict is the obvious answer. The point of the class
is that nobody outside has to know or care.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 4 day 1" && git push
```

---

## Predict-then-run

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{name} says woof"

d = Dog("Rex")
print(d.bark())
```

One error. Say which line, which error, and why — before running it. It is the mistake
you will make five times today.

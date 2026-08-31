# Day 3 — Labels instead of positions

> **By the end of today** you can store data with names attached, and print it in
> neat columns.

A list says *"the third thing"*. A dict says *"the price"*. Once your data has more
than one field per item, counting positions stops working and starts causing bugs.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on Python dictionaries — 25 min]`
- [ ] `[INSTRUCTOR: source on nested data (lists of dicts) — 15 min]`

---

## What you need to know

### A dict maps keys to values

```python
contact = {
    "name": "Ana Silva",
    "email": "ana@example.com",
    "city": "Lisbon",
}

print(contact["name"])          # Ana Silva
```

Square brackets again, but a **key** goes inside instead of a position. Keys are
almost always strings. Order does not matter — there is no "third item" in a dict, and
you never want one.

### Adding, changing, and the error you will hit

```python
contact["phone"] = "555-0182"       # adds it - the key did not exist
contact["city"] = "Porto"           # changes it - the key did exist
print(contact["fax"])               # KeyError: 'fax'
```

Same square brackets for both adding and changing. Python does not care which you
meant, which is convenient and occasionally a bug.

`KeyError` is the dict version of `IndexError` and means the same thing: *you asked for
something that is not there.*

### `.get()` — asking safely

```python
print(contact.get("fax"))               # None       - no error
print(contact.get("fax", "unknown"))    # unknown    - your fallback
```

Use `.get()` whenever you are not certain the key exists — which is most of the time
when the key came from a person.

### Checking and looping

```python
print("email" in contact)       # True   - checks KEYS, not values

for key in contact:                     # keys
    print(key)

for value in contact.values():          # values
    print(value)

for key, value in contact.items():      # both - this is the one you want
    print(f"{key}: {value}")
```

### Counting things — a pattern worth memorising

This shape comes up constantly, and it is a genuine interview question:

```python
words = ["apple", "banana", "apple"]

counts = {}
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1

print(counts)       # {'apple': 2, 'banana': 1}
```

Read it as: *"seen it before? add one. Never seen it? start at one."*

`sorted(counts)` gives you the keys in alphabetical order, which is how you print a
count table that does not change between runs.

### A list of dicts — how real data looks

This is the shape of nearly every dataset you will meet, and it is exactly what comes
back from a web API in week 5:

```python
students = [
    {"name": "Ana", "score": 92},
    {"name": "Ben", "score": 78},
]

for student in students:
    print(student["name"], student["score"])
```

The loop hands you one **dict** each time round, and you reach into it with a key.
Two levels: the list holds records, each record holds fields.

### Lining up columns

Money got `:.2f`. Columns get a width and a direction:

```python
print(f"{'Ana':<10}")     # 'Ana       '   <  left, padded to 10
print(f"{92:>6}")         # '    92'       >  right, padded to 6
print(f"{'x':^7}")        # '   x   '      ^  centred
```

Numbers go right, text goes left. That is a convention, not a rule, and it is why
every well-made table you have ever seen looks the way it does.

You can combine them: `f"{price:>8.2f}"` means *right-aligned, 8 wide, 2 decimals.*

---

## Exercises

```bash
pytest week-02/day-3 -v
```

### 1. `contact.py`

The file already contains the `contact` dict above. Print:

```
Name: Ana Silva
Email: ana@example.com
City: Lisbon
```

Then add a `phone` of `555-0182` and print:

```
Fields: 4
Phone: 555-0182
Has fax: False
```

### 2. `counts.py`

The file already contains:

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
```

Count them and print, **in alphabetical order**:

```
apple: 3
banana: 2
cherry: 1
```

### 3. `lookup.py`

The file already contains a `capitals` dict. Ask `Country: ` and print:

```
Capital: Paris
```

If the country is not in the dict, print `Capital: unknown`. Use `.get()` — your
program must not crash on a country nobody has heard of.

### 4. `records.py`

The file already contains a list of four student dicts. Print:

```
NAME         SCORE
------------------
Ana             92
Benjamin        78
Cara            85
Dev             65
------------------
Average:      80.0
```

- Names left-aligned in 12 characters, scores right-aligned in 6
- The rules are 18 dashes
- The average has one decimal place and lines up with the scores

Work the average out with an accumulator — the whole point is that you never typed a
score into your own code.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 2 day 3" && git push
```

Read `milestone/README.md` tonight. Friday's report is today's `records.py` with more
columns and a ranking, and it is much easier if it is not a surprise.

---

## Predict-then-run

```python
d = {"a": 1, "b": 2}
print(d["c"])
print(d.get("c"))
print("a" in d)
print(1 in d)
```

That last one is the interesting one. `1` *is* in there — as a value. So why is the
answer what it is? Being clear on what `in` checks for a dict will save you an hour
later this week.

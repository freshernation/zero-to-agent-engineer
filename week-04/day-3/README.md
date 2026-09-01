# Day 3 — Writing tests, and testing your tests

> **By the end of today** you can write a test suite, and tell whether it is any good.

Every Wednesday so far, tests were something that happened *to* you. Today you write
them — and then your suite is run against **deliberately broken code** to see whether it
notices.

This is the day with the highest ratio of interview value to effort in the whole course.
"How do you know your tests are any good?" is a question most junior candidates cannot
answer at all.

---

## Read / watch first

- [ ] [**Writing tests with pytest**](../../content/week-04/day-3/writing-tests-with-pytest.md) — 30 min · docs: [pytest — Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [ ] [**pytest fixtures and `parametrize`**](../../content/week-04/day-3/pytest-fixtures-and-parametrize.md) — 15 min · docs: [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

---

## What you need to know

### A test is a function that asserts

```python
def test_square_area():
    assert Square(3).area() == 9
```

- the file is named `test_something.py`
- the functions are named `test_something`
- `assert` is the whole mechanism: true passes, false fails

Run them with `pytest week-04/day-3 -v`.

### Testing that something raises

```python
import pytest

def test_negative_radius_is_rejected():
    with pytest.raises(ValueError):
        Circle(-1)
```

The test **passes** when the code inside raises. You can check the message too:

```python
    with pytest.raises(ValueError, match="must be positive"):
        Circle(-1)
```

### `parametrize` — the same test, many values

```python
@pytest.mark.parametrize("side,expected", [
    (1, 1),
    (3, 9),
    (10, 100),
])
def test_square_area(side, expected):
    assert Square(side).area() == expected
```

Three tests, one function, and each failure is reported separately so you know exactly
which value broke.

### Fixtures — shared setup

```python
@pytest.fixture
def shapes():
    return [Circle(1), Square(2), Circle(3)]

def test_total_area(shapes):
    assert total_area(shapes) == 45.4
```

Ask for the fixture by putting its name in the test's arguments. Each test gets a fresh
one, so tests cannot contaminate each other.

### What makes a test good

Most beginner suites are long and useless because every test checks the same easy path.
Four questions worth asking of each test you write:

| Question | Why |
|---|---|
| **Would this fail if the code were wrong?** | The only question that really matters |
| **Am I testing a boundary?** | Bugs live at 0, 1, empty, the last item, the exact limit |
| **Am I testing the failure path?** | The error case is code too, and it is less exercised |
| **Would two different bugs both pass this?** | Then the test is not pinning anything down |

### The trap in today's exercise

`Circle(2).area()` is `12.57`. `Circle(2).circumference()` is **also** `12.57`.

So a suite that only ever tests radius 2 cannot tell area and circumference apart. If
someone swapped the two formulas, that suite would go green and the bug would ship.

**Test more than one value.** Today you find out the hard way whether you did.

---

## Exercises

```bash
pytest week-04/day-3 -v          # grades your suites
python3 week-04/day-3/check_my_tests.py    # runs them and shows the output
```

The first command tells you whether your tests would catch a bug. The second
runs them normally so you can see them pass while you work.

### 1. `test_shapes.py` — the main event

`shapes.py` is in this folder. It is **correct** and you must not change it. Write
`test_shapes.py` to test it.

Your suite has to satisfy three things:

1. **It passes** against `shapes.py` as given.
2. **It fails** against each of six broken versions. Your tests never see them — but
   today's tests break `shapes.py` in six ways behind your back and check your suite
   notices every one:

   | # | The bug planted |
   |---|---|
   | 1 | `Circle.area` returns the circumference formula |
   | 2 | `Circle` stops rejecting a radius of zero or less |
   | 3 | `Square.perimeter` returns three times the side |
   | 4 | `total_area` quietly ignores the last shape |
   | 5 | `largest` returns the **smallest** shape |
   | 6 | `largest` crashes on an empty list instead of returning `None` |

3. **It contains** at least eight test functions, at least one `pytest.raises`, and at
   least one `@pytest.mark.parametrize`.

You cannot pass this by writing many tests. You pass it by writing tests that would
**notice**.

### 2. `stats.py` and `test_stats.py` — tests first

Write the tests **before** the code. Genuinely — it feels backwards for about twenty
minutes and then it does not.

`stats.py` must provide:

| Function | Returns |
|---|---|
| `mean(numbers)` | the average, rounded to 2dp; raises `ValueError("No numbers")` if empty |
| `median(numbers)` | the middle value; the mean of the middle two when there is an even count; raises `ValueError("No numbers")` if empty |
| `mode(numbers)` | the most common value; the **smallest** one if several tie |
| `spread(numbers)` | the biggest minus the smallest; `0` for a single number |

```python
mean([1, 2, 3])             # 2.0
median([1, 3, 2])           # 2        <- note: sort it first
median([1, 2, 3, 4])        # 2.5
mode([1, 2, 2, 3])          # 2
mode([1, 1, 2, 2])          # 1        <- tie, so the smallest
spread([4, 1, 9])           # 8
```

`test_stats.py` needs at least six test functions and must pass against your own
`stats.py`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 4 day 3" && git push
```

Read the milestone spec tonight.

---

## Predict-then-run

```python
def test_it_works():
    result = 2 + 2
    assert result

def test_it_also_works():
    assert [1, 2, 3]
```

Both pass. Neither tests anything. Explain what `assert` actually checks, and why these
two are the most common form of fake test in real codebases.

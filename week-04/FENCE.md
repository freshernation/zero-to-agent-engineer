# Week 4 — Concept fence

## Allowed

**Everything from Weeks 1–3**, plus:

- **Classes** — `class`, `__init__`, `self`, attributes, methods
- **Dunder methods** — `__repr__`, `__str__`, `__eq__`, `__len__`
- **Composition** — a class holding a list of other objects
- **Type hints** — `def total(items: list) -> float:`, `str`, `int`, `float`, `bool`,
  `list`, `dict`, `None`, `Optional`
- **pytest** — `assert`, test functions, test classes, `pytest.raises`,
  `@pytest.mark.parametrize`, fixtures with `@pytest.fixture`, `tmp_path`
- `isinstance()`, `hasattr()`

## Not yet

Inheritance beyond one level · abstract base classes · `@property` · `@staticmethod` /
`@classmethod` · `@dataclass` · metaclasses · `__slots__` · multiple inheritance ·
operator overloading beyond the four above · mocking and `unittest.mock` · coverage
tools · async · any third-party library except pytest

---

## The question this week keeps asking

**Does this need to be a class?**

A class earns its place when data and the behaviour that acts on it belong together and
travel together. A `BankAccount` has a balance, and depositing changes it — those two
things should not be able to drift apart.

A class is the wrong answer when you have a function wearing a costume. If a class has
one method and no state worth protecting, it should have been a function. You will
write one of those this week and be asked to defend it on Friday.

# Day 2 — Refusing to trust a response

> **By the end of today** you never touch API data until something has checked it is
> the shape you were promised.

---

## Read / watch first

- [ ] [**pydantic v2 basics**](../../content/week-05/day-2/pydantic-basics.md) — 30 min · docs: [pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)
- [ ] [**pydantic validators**](../../content/week-05/day-2/pydantic-validators.md) — 15 min · docs: [Validators](https://docs.pydantic.dev/latest/concepts/validators/)

---

## What you need to know

### The problem

```python
users = requests.get(url).json()
for user in users:
    print(user["email"].upper())
```

This works. Until the day one user has `"email": null`, and you get
`AttributeError: 'NoneType' object has no attribute 'upper'` — in the middle of a loop,
three functions from where the bad data came in, at whatever hour the other team
deployed.

Dicts have no shape. Nothing in the code above says what a user *is*, so nothing can
notice when one is wrong.

### A model says what the shape is

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    city: str
```

```python
user = User(id=1, name="Ana", email="ana@example.com", city="Lisbon")
print(user.name)        # Ana        <- attribute, not user["name"]
```

Those type hints stop being documentation and start being **enforced**. This is the
same annotation syntax as week 4, doing a completely different job.

### Building one from a response

```python
raw = requests.get(f"{base}/users/1").json()
user = User.model_validate(raw)
```

If the data is wrong, it raises `ValidationError` **immediately**, at the boundary,
naming the field and the problem — instead of a mystery `AttributeError` somewhere else
an hour later.

For a list:

```python
users = [User.model_validate(item) for item in raw_list]
```

### Conversion for free

```python
User(id="1", ...)       # id becomes the integer 1
```

pydantic coerces where it is unambiguous, which handles the very common case of an API
sending numbers as strings. It will not invent data: `id="banana"` raises.

### Optional and defaults

```python
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool = True               # a default makes the field optional
    description: Optional[str] = None   # may be absent OR null
```

`Optional[str] = None` is how you say *"this may legitimately be missing"*. Anything
without a default is **required**, and that is the useful default — a required field is
a promise you get told about when it breaks.

### Constraints

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0, le=1000)
```

`gt` greater than · `ge` greater or equal · `lt` · `le` · `min_length` · `max_length`.

### Your own rules

```python
from pydantic import field_validator

class User(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def email_must_have_an_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain @")
        return value
```

Validators **return the value** — which means they can clean it up as well as check it.

### Catching it

```python
from pydantic import ValidationError

try:
    user = User.model_validate(raw)
except ValidationError as error:
    print(error)        # names the field, the rule, and what it got
```

### Back to plain data

```python
user.model_dump()       # {'id': 1, 'name': 'Ana', ...}  - for saving as JSON
```

### Where validation belongs

**At the boundary, once.** Validate the moment data enters your program, and everything
after that point can trust it completely. Validating in five places means five chances
to disagree with yourself.

---

## Exercises

```bash
pytest week-05/day-2 -v
```

### 1. `models.py`

Three models.

**`User`** — `id: int`, `name: str` (at least 1 character), `email: str` (must contain
`@`), `city: str`.

**`Product`** — `id: int`, `name: str`, `price: float` (greater than 0),
`category: str`, `in_stock: bool` defaulting to `True`.

**`Order`** — `id: int`, `user_id: int`, `product_id: int`, `quantity: int` (at least 1).

### 2. `parse.py`

| Function | Returns |
|---|---|
| `parse_user(raw)` | a `User`, or raises `ValidationError` |
| `parse_users(raw_list)` | a list of `User`s — **skipping** any that fail |
| `parse_products(raw_list)` | same, for `Product` |
| `count_bad(raw_list, model)` | how many records fail validation |

`parse_users` skipping bad records rather than exploding is a real decision, and it is
the right one when three good users are more useful than none. It is the wrong one for
a bank transfer. Know which situation you are in.

### 3. `pipeline.py`

Putting yesterday and today together.

| Function | Returns |
|---|---|
| `fetch_users(base_url)` | a list of validated `User` objects |
| `fetch_products(base_url, category=None)` | a list of validated `Product` objects |
| `total_stock_value(base_url)` | the price of every in-stock product added up, to 2dp |

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 5 day 2" && git push
```

---

## Predict-then-run

```python
class User(BaseModel):
    id: int
    name: str

print(User(id="7", name="Ana"))
print(User(id=7.0, name="Ana"))
print(User(id=7.5, name="Ana"))
print(User(id="seven", name="Ana"))
```

Two of those succeed, one is interesting, and one raises. Work out pydantic's rule for
when it will convert and when it refuses — "it converts if nothing is lost" is close,
and the third line is where it gets precise.

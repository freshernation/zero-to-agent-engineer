# Day 3 — Secrets, retries, and the unglamorous 80%

> **By the end of today** your code keeps its keys out of git, gives up gracefully, and
> tries again when trying again is the right answer.

None of today is clever. All of it is the difference between something that works on
your laptop and something you would let other people depend on.

---

## Read / watch first

- [ ] [**Environment variables and `.env` files**](../../content/week-05/day-3/environment-variables.md) — 20 min · docs: [`os.environ`](https://docs.python.org/3.14/library/os.html#os.environ)
- [ ] [**Retries and backoff**](../../content/week-05/day-3/retries-and-backoff.md) — 15 min · docs: [`time.sleep()`](https://docs.python.org/3.14/library/time.html#time.sleep)

---

## What you need to know

### Never put a key in your code

```python
API_KEY = "sk-ant-api03-real-key-here"      # now it is in git forever
```

Git keeps history. Deleting the line later does not remove it — it is still in every
clone, and scanners find published keys within minutes.

Keys live in the **environment**:

```python
import os

api_key = os.environ["COURSE_API_KEY"]      # KeyError if missing
api_key = os.getenv("COURSE_API_KEY")       # None if missing
api_key = os.getenv("COURSE_API_KEY", "")   # "" if missing
```

### `.env` for local work

Typing `export` before every run gets old. Put them in a file:

```
# .env
COURSE_API_KEY=course-key-123
API_BASE_URL=http://127.0.0.1:8765
```

```python
from dotenv import load_dotenv

load_dotenv()                                   # reads .env into the environment
api_key = os.getenv("COURSE_API_KEY")
```

**`.env` goes in `.gitignore`. Always. First.** It is already in this repo's.

Ship a `.env.example` alongside it with the *names* and no values — so someone cloning
your project knows what they need without you handing them your keys.

### Fail loudly when a key is missing

```python
api_key = os.getenv("COURSE_API_KEY")
if not api_key:
    raise RuntimeError(
        "COURSE_API_KEY is not set. Copy .env.example to .env and fill it in."
    )
```

A missing key that turns into a 401 five function calls later wastes twenty minutes
every time. Check it at startup and say what to do about it.

### Retries — and when not to

Networks fail temporarily. A single 503 usually means "try again in a second", not
"give up".

```python
import time

def fetch_with_retry(url, attempts=3, delay=0.5):
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                return response          # 200 or 404 - both are real answers
        except requests.exceptions.RequestException:
            pass                         # network trouble, worth retrying

        if attempt < attempts - 1:
            time.sleep(delay * (2 ** attempt))      # 0.5, 1.0, 2.0 - backoff
    return None
```

Two decisions in there are the whole lesson:

**Retry 5xx, not 4xx.** A 500 is their problem and might pass. A 404 is *your* problem
and will still be a 404 in a second — retrying it just wastes time and their capacity.

**Back off exponentially.** `delay * (2 ** attempt)` doubles the wait each time. If a
service is struggling, a thousand clients retrying instantly is what turns a wobble
into an outage.

### A client class

Once you have a base URL, a key, a timeout and a retry policy, passing all four to
every function gets silly. Week 4 has an answer:

```python
class ApiClient:
    def __init__(self, base_url, api_key=None, timeout=5, retries=3):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"
        ...

    def get(self, path, params=None):
        ...
```

`requests.Session` reuses the underlying connection between calls, which is faster, and
holds headers so you set them once.

This is the shape of every SDK you will ever use — including the Anthropic client you
meet on Monday. Writing one yourself now is why that one will not feel like magic.

### One custom exception

```python
class ApiError(Exception):
    pass
```

That is the entire definition. Raising `ApiError` rather than `ValueError` lets a caller
say "catch anything the API layer throws" without also swallowing genuine bugs.

---

## Exercises

```bash
pytest week-05/day-3 -v
```

### 1. `config.py`

| Function | Returns |
|---|---|
| `get_api_key()` | the value of `COURSE_API_KEY`, or raises `RuntimeError` naming it |
| `get_base_url()` | `API_BASE_URL`, defaulting to `http://127.0.0.1:8765` |
| `load_config()` | a dict with `api_key` and `base_url` |

`get_api_key`'s error message must contain `COURSE_API_KEY`, so whoever hits it knows
what to set.

### 2. `retry.py`

| Function | Returns |
|---|---|
| `fetch_with_retry(base_url, path, attempts=3, delay=0.05)` | the parsed body, or `None` if every attempt failed |
| `attempts_used(base_url, path, attempts=3, delay=0.05)` | how many attempts it actually took |
| `should_retry(status_code)` | `True` for 5xx, `False` for everything else |

`/flaky` fails twice and then succeeds — with three attempts it should come back with
data, having used all three.

### 3. `client.py`

**`ApiError(Exception)`** — one line.

**`ApiClient(base_url, api_key=None, timeout=5, retries=3)`**

| Member | Does |
|---|---|
| `get(path, params=None)` | returns the parsed body; raises `ApiError` on a 4xx or an exhausted retry |
| `get_or_none(path, params=None)` | the same, but returns `None` instead of raising |
| `users()` | the list of users |
| `user(user_id)` | one user, or `None` |
| `products(category=None)` | the products |

It must use a `requests.Session`, send the `Authorization` header when a key was given,
and retry 5xx.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 5 day 3" && git push
```

Then run `git log -p | grep -i "key"` on your own repo and make sure you find nothing
you would not want on a billboard.

---

## Predict-then-run

```python
for attempt in range(3):
    print(f"attempt {attempt}, waiting {0.5 * (2 ** attempt)}")
```

Now change it to a hundred attempts and read the last number out loud. Exponential
backoff needs a **cap**, and nearly every first implementation forgets one. Where would
you put it?

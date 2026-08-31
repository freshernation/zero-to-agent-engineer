# Week 5 — Concept fence

## Allowed

**Everything from Weeks 1–4**, plus:

- `requests` — `get()`, `.status_code`, `.json()`, `.text`, `.headers`,
  `raise_for_status()`, `params=`, `headers=`, `timeout=`
- `requests.exceptions` — `Timeout`, `ConnectionError`, `HTTPError`, `RequestException`
- `requests.Session`
- **pydantic v2** — `BaseModel`, field types, `Field(...)`, `field_validator`,
  `model_validate`, `model_dump`, `ValidationError`, `Optional`, `list[Model]`
- `os.environ` / `os.getenv`, `python-dotenv`'s `load_dotenv`
- `time.sleep` for backoff
- **one** custom exception class (`class ApiError(Exception): pass`)

## Not yet

`async` / `await` and `httpx` async · building your own API (week 11) · OAuth flows ·
GraphQL · webhooks · `asyncio` · databases · `pandas` · LangChain or any LLM library
(week 6) · pydantic `Settings` · retry libraries like `tenacity` — you write the loop
yourself this week

---

## The practice API

Everything this week talks to a small web server that runs on your own machine:

```bash
python3 week-05/server.py
```

Then `http://127.0.0.1:8765/users` in a browser. The tests start their own copy, so you
only need to run it when you want to poke at it by hand.

| Endpoint | Does |
|---|---|
| `/users` | four users |
| `/users/<id>` | one user, or **404** |
| `/products?category=tools` | products, optionally filtered |
| `/orders?user_id=1` | orders, optionally filtered |
| `/secret` | **401** unless you send the right `Authorization` header |
| `/slow` | takes three seconds |
| `/flaky` | **503** twice, then succeeds |
| `/broken` | 200, and the body is not valid JSON |
| `/error` | **500** |

The last four exist because real APIs do all of that, and code that only handles the
happy path is code that has not been finished.

# Day 1 — HTTP and `requests`

> **By the end of today** you can fetch data from a web API and tell the difference
> between "it worked", "it politely refused", and "it fell over".

---

## Read / watch first

- [ ] [**How HTTP works**](../../content/week-05/day-1/how-http-works.md) — 25 min · docs: [MDN — An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [ ] [**The `requests` library**](../../content/week-05/day-1/the-requests-library.md) — 20 min · docs: [requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)

---

## What you need to know

### Start the practice API

```bash
python3 week-05/server.py
```

Leave it running in one terminal and work in another. Visit
`http://127.0.0.1:8765/users` in a browser — that is the same request your code will
make, and seeing it in a browser first makes the code feel much less magical.

### The shape of a request

```python
import requests

response = requests.get("http://127.0.0.1:8765/users")

print(response.status_code)     # 200
print(response.json())          # [{'id': 1, 'name': 'Ana Silva', ...}, ...]
```

`.json()` parses the response body into ordinary Python — usually a list of dicts,
which is week 2's material arriving from a thousand miles away.

### Status codes

The number tells you what happened, and the first digit tells you who to blame.

| Code | Means | Whose fault |
|---|---|---|
| **200** | OK | — |
| **201** | Created | — |
| **400** | Bad request | yours |
| **401** | Unauthorized — no or wrong credentials | yours |
| **403** | Forbidden — credentials fine, permission denied | yours |
| **404** | Not found | usually yours |
| **429** | Too many requests — slow down | yours |
| **500** | Server error | theirs |
| **503** | Service unavailable, try later | theirs |

**A 404 is not an exception.** `requests` returns you a perfectly good response object
with `status_code == 404`; nothing raises. If you call `.json()` on it you get the
error body, not your data. Checking the status is *your* job:

```python
if response.status_code == 200:
    return response.json()
return None
```

There is a shortcut that raises for you:

```python
response.raise_for_status()     # raises requests.HTTPError for 4xx and 5xx
```

Use it when a failure genuinely should stop everything. Use the explicit check when
"not found" is a normal answer you want to handle.

### Query parameters

Do not build URLs by gluing strings together:

```python
url = f"{base}/products?category={category}"          # fragile
response = requests.get(f"{base}/products",
                        params={"category": category}) # correct
```

`params=` escapes anything awkward — spaces, ampersands, non-English characters — that
would otherwise quietly corrupt your URL.

### Headers

```python
response = requests.get(url, headers={"Authorization": "Bearer some-key"})
```

Headers carry metadata about the request: who you are, what format you want back. The
practice API's `/secret` endpoint wants exactly the header above.

### Timeouts — the one everybody forgets

```python
requests.get(url)                   # will wait forever. Genuinely forever.
requests.get(url, timeout=5)        # gives up after 5 seconds
```

**Always pass `timeout`.** A request with no timeout is how a program hangs at three in
the morning with nothing in the logs. `requests` raises `requests.exceptions.Timeout`
when it runs out, which you can catch.

Try it on `/slow`, which takes three seconds, with a timeout of one.

---

## Exercises

```bash
pytest week-05/day-1 -v
```

Every function takes `base_url` as its first argument. Do not hard-code the address —
that is what makes the same code work against the practice server today and a real API
in week 11.

### 1. `fetch.py`

| Function | Returns |
|---|---|
| `get_users(base_url)` | the list of user dicts |
| `get_user(base_url, user_id)` | one user dict, or `None` if the API says 404 |
| `get_products(base_url, category=None)` | all products, or just that category |

`get_products` must use `params=`, not an f-string URL.

### 2. `status.py`

| Function | Returns |
|---|---|
| `status_of(base_url, path)` | the status code as an `int` |
| `is_ok(base_url, path)` | `True` for any 2xx code, `False` otherwise |
| `fetch_json(base_url, path)` | the parsed body for a 2xx, `None` for anything else |

`is_ok` must accept **any** 2xx, not just 200 exactly.

### 3. `careful.py`

| Function | Returns |
|---|---|
| `fetch_with_timeout(base_url, path, timeout)` | the parsed body, or the string `"timed out"` if it took too long |
| `get_secret(base_url, api_key)` | the parsed body, or `None` if the key is rejected |

The practice API's key is `course-key-123` and it wants
`Authorization: Bearer <key>`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 5 day 1" && git push
```

---

## Predict-then-run

With the server running:

```python
import requests
r = requests.get("http://127.0.0.1:8765/users/99")
print(r.status_code)
print(r.json())
data = r.json()
print(data["name"])
```

Four lines, one crash, and the crash is not where a beginner expects. Explain what
`.json()` gave you back on a 404 and why that is more dangerous than an exception
would have been.

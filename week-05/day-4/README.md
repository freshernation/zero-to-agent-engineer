# Day 4 — Combining endpoints

> **By the end of today** you can answer a question no single endpoint answers, and
> debug the three failures that only happen once your code leaves the machine.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on combining API data — 15 min]`

---

## What you need to know

### One question, three endpoints

*"How much has each customer spent?"* is not an endpoint. The data is spread across
three:

- `/users` — who they are
- `/orders?user_id=1` — what they bought
- `/products` — what those things cost

Combining them is most of what backend work actually is. The pattern:

1. Fetch the pieces
2. Build a **lookup** so you can join them
3. Walk the main list, reaching into the lookup

```python
products = get_products(base_url)
by_id = {p["id"]: p for p in products}      # week 3's dict comprehension

for order in orders:
    product = by_id[order["product_id"]]
    line_total = order["quantity"] * product["price"]
```

That `by_id` dict is the whole trick. Without it you would search the product list once
per order — which is fine for four products and catastrophic for forty thousand.

### Fetch once, not in a loop

```python
for order in orders:                                    # BAD
    product = requests.get(f"{base}/products/{order['product_id']}").json()
```

One HTTP request per order. Ten orders, ten round trips, ten chances to fail. Fetch the
product list **once**, build the lookup, then loop over local data.

This has a name — the **N+1 problem** — and it is one of the most common causes of slow
software in the world. It is also a question you will get asked in interviews, so it is
worth being able to say the name out loud.

### Partial failure

Three calls means three chances to fail, and "the whole report crashed because one
endpoint was down" is rarely the right answer. Decide, per call:

- **Essential** — no users, no report. Fail loudly.
- **Enrichment** — no product names? Show the IDs and carry on.

Making that choice deliberately, rather than letting whichever exception escapes first
decide for you, is the difference between a service and a script.

---

## Exercises

```bash
pytest week-05/day-4 -v
```

### 1. `merge.py`

| Function | Returns |
|---|---|
| `get_orders(base_url, user_id)` | that user's raw order dicts |
| `enrich_orders(base_url, user_id)` | one dict per order with `product`, `quantity`, `price`, `line_total` |
| `user_summary(base_url, user_id)` | `name`, `city`, `order_count`, `total_spent` |
| `ranked_customers(base_url)` | a summary per user, highest `total_spent` first |

`enrich_orders` must fetch the product list **once**. There is a test that counts.

---

## Debugging, round five

| File | Should print |
|---|---|
| `broken_1.py` | `Missing user: none found` |
| `broken_2.py` | `Attempts: 1` |
| `broken_3.py` | `City: Lisbon` |

Start the server first — these talk to it.

```bash
python3 week-05/server.py
```

- **`broken_1.py`** trusts a response without checking it. The crash is a `KeyError`,
  which is a strange thing to get from a web request until you realise what a 404's
  body actually contains.
- **`broken_2.py`** retries something that will never succeed. No error, just wasted
  time — and on a real API, wasted quota.
- **`broken_3.py`** has **one bug, hidden by one bad habit.** Fix the habit first and
  the bug will introduce itself.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 5 day 4" && git push
```

---

## Predict-then-run

```python
products = [{"id": 10, "name": "Widget"}, {"id": 11, "name": "Gadget"}]
orders = [{"product_id": 10}, {"product_id": 99}]

by_id = {p["id"]: p for p in products}
for order in orders:
    print(by_id[order["product_id"]]["name"])
```

One line prints, then it stops. The order referred to a product that does not exist —
which happens constantly in real data. What are your three options, and which would you
pick for a report a person is going to read?

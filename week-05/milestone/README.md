# Week 5 Milestone — The Customer Report

> Three endpoints in. One report out. It works when the API misbehaves, and it says so
> when it cannot.

---

## The files

| File | Holds |
|---|---|
| `models.py` | `User`, `Product`, `Order` — pydantic models |
| `api.py` | `ApiError` and `ApiClient` — everything that touches the network |
| `report.py` | The program. All the printing. |

Same layering rule as weeks 3 and 4, now with a third layer: **network, then
validation, then presentation.** Data is validated once, on the way in, and everything
downstream can trust it.

---

## `models.py`

| Model | Fields |
|---|---|
| `User` | `id: int`, `name: str` (≥1 char), `email: str` (contains `@`), `city: str` |
| `Product` | `id: int`, `name: str`, `price: float` (>0), `category: str`, `in_stock: bool = True` |
| `Order` | `id: int`, `user_id: int`, `product_id: int`, `quantity: int` (≥1) |

## `api.py`

**`ApiError(Exception)`**

**`ApiClient(base_url, api_key=None, timeout=5, retries=3)`** — uses a
`requests.Session`, sends `Authorization: Bearer <key>` when given one, retries 5xx
with a backoff, raises `ApiError` on a 4xx or an exhausted retry.

| Method | Returns |
|---|---|
| `get(path, params=None)` | the parsed body, or raises `ApiError` |
| `users()` | `list[User]` |
| `products()` | `list[Product]` |
| `orders(user_id=None)` | `list[Order]` |

The three above return **validated models**, skipping any record that fails validation.
A single malformed product must not lose you the report.

## `report.py`

| Function | Returns |
|---|---|
| `build_rows(client, user, products_by_id, orders)` | one dict per order: `product`, `quantity`, `price`, `line_total` |
| `summarise(client)` | a list of per-user summaries, biggest spender first |
| `render(summaries)` | the whole report as a **single string** |
| `main()` | prints it, or prints a clear failure |

`render` returning a string rather than printing is deliberate: it makes the report
testable without capturing stdout, which is the same reason `expenses.py` never printed
in week 3.

### The output

```
CUSTOMER ORDER REPORT
==================================================
Ana Silva            Lisbon
  Widget                2 x $   4.50 = $     9.00
  Doohickey             1 x $   3.25 = $     3.25
  2 orders, $12.25

Ben Okafor           Lagos
  Thingummy             3 x $  89.00 = $   267.00
  1 order, $267.00

Cara Diaz            Bogota
  No orders

Dev Patel            Mumbai
  Gadget                1 x $  12.00 = $    12.00
  1 order, $12.00

==================================================
TOP CUSTOMERS
1. Ben Okafor          $   267.00
2. Ana Silva           $    12.25
3. Dev Patel           $    12.00
Total revenue: $291.25
```

| Line | Format |
|---|---|
| Rules | 50 `=` |
| User header | `{name:<20} {city}` |
| Order line | `  {product:<20}{quantity:>3} x ${price:>7.2f} = ${line_total:>9.2f}` |
| Summary | `  2 orders, $12.25` — **`1 order`** singular |
| No orders | `  No orders` and nothing else — no summary line |
| Top line | `{rank}. {name:<20}${total:>9.2f}` |
| Blank line | one after each user, none after the last before the rule |

Top customers is the **top three**, biggest first.

### When the API is down

`main()` must not produce a traceback. If the users call fails:

```
Could not reach the API at http://127.0.0.1:9999
```

Nothing else. The address in the message is the one it actually tried.

---

## Check it

```bash
python3 week-05/server.py          # in one terminal
pytest week-05/milestone -v        # in another
```

Twenty-six tests, including one that points the client at a dead port and one that
feeds it a deliberately malformed product.

---

## Then make it good

- [ ] `api.py` and `models.py` contain no `print()`
- [ ] `report.py` contains no `requests`
- [ ] Every network call has a `timeout`
- [ ] No key, real or fake, anywhere in the source
- [ ] `render()` builds a string; only `main()` prints
- [ ] The product list is fetched **once**

Run `ai/editor.md` over all three files.

---

## Ship it

```bash
git add -A && git commit -m "week 5 milestone: customer report" && git push
```

---

## Friday

Three phases as usual. The mutate phase this week is a fourth endpoint, and the debug
phase is a seeded bug in code that talks to a network — which is a different kind of
hunt, because now "it works on my machine" and "it works" have come apart.

# Day 3 — Seeing inside a request

> **By the end of today** you can answer "what happened at 3pm yesterday" from the logs
> alone.

---

## Read / watch first

- [ ] [**Structured logging and tracing**](../../content/week-11/day-3/logging-and-tracing.md) — 25 min · docs: [`logging`](https://docs.python.org/3.14/library/logging.html)

---

## What you need to know

### `print` does not survive contact with production

It goes to stdout, has no timestamp, no severity, and no way to find one request among
thousands. Fine on your laptop, useless the moment somebody else is using the thing.

### Structured logs are JSON, not sentences

```python
print("Answered question in 1.2s")                       # unsearchable
log("info", "answered", duration_ms=1200, sources=2)     # searchable
```

```json
{"level": "info", "event": "answered", "duration_ms": 1200, "sources": 2}
```

The difference is that you can ask *"show me every request over 5000ms"* and get an
answer. With sentences you can only grep, and grep cannot compare numbers.

**Log events, not prose.** `"answered"` is an event. `"Successfully answered the user's
question!"` is prose with an event hidden in it.

### The request id

```python
request_id = uuid4().hex[:12]
```

One id, generated when the request arrives, attached to **every** log line for that
request. It is what turns "something broke" into "here is the whole story of that one
request", and it is the single highest-value thing on this page.

Without it, a service handling ten requests a second produces logs that are interleaved
and unreadable. With it, you filter by the id and see one story.

### Never log the secret

You masked it yesterday. The same rule applies to every log line, and it is easier to
break here — a helpful `log("debug", "calling", headers=headers)` puts your key in the
log service forever.

### A trace is a tree of timings

A log line says something happened. A trace says how long it took and what it was inside:

```
request                     1240ms
  retrieve                   140ms
    embed                     12ms
    search                   126ms
  generate                  1090ms
```

Now "it is slow" becomes "generation is 88% of it, and retrieval is not the problem" —
which is a completely different conversation, and the only one worth having about
performance.

You are writing a small tracer today. LangSmith, Langfuse and OpenTelemetry do this
properly, and after today they will look like a nicer version of something you already
understand.

### Timing needs an injected clock

```python
tracer = Tracer(request_id, clock=time.monotonic)
```

Real time in production, a fake clock in tests. Dependency injection, for the fourth
time — and here it is the only way to write a test about durations that is not flaky.

Use `time.monotonic`, not `time.time`. Wall-clock time can go backwards when the machine
syncs with a time server, and a negative duration in a chart is a genuinely confusing
half hour.

---

## Exercises

```bash
pytest week-11/day-3 -v
```

### 1. `logs.py`

| Function | Returns |
|---|---|
| `new_request_id()` | 12 lowercase hex characters |
| `redact(fields, secret_keys=("api_key", "authorization", "token"))` | the fields with those values replaced by `"****"`, case-insensitively, including nested dicts |
| `log_line(level, event, **fields)` | a JSON string with `level`, `event` and the fields, redacted |
| `parse(line)` | the JSON back to a dict — for the tests, and for you |

### 2. `tracer.py`

**`Tracer(request_id, clock)`**

| Member | Does |
|---|---|
| `span(name, **metadata)` | a context manager; nests inside whatever is already open |
| `to_dict()` | `{"request_id", "spans": [...]}` — a tree, each with `name`, `duration_ms`, `metadata`, `children` |
| `total_ms()` | the whole request |
| `flatten()` | `[(depth, name, duration_ms), ...]`, in the order they started |
| `slowest()` | the name of the slowest **top-level** span |

A span object has `set(key, value)` for adding metadata while it runs.

`clock` returns a float in seconds; durations are whole milliseconds.

A span whose body **raises** must still be closed and recorded, with
`metadata["error"]` set to the exception's message. A tracer that loses its data when
something goes wrong is a tracer that is missing exactly the runs you care about.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 3" && git push
```

---

## Predict-then-run

Trace a request with a retrieval span and a generation span, and print `flatten()`.

Now ask: if this were 4 seconds and a user complained, what would you change? You can
answer that in five seconds from the trace and not at all from the logs — which is the
whole reason both exist.

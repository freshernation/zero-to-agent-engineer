# Day 2 — Configuration, health, and deploying

> **By the end of today** your service can be configured from outside, says whether it
> is healthy, and has everything a platform needs to run it.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on twelve-factor config and deployment — 25 min]`

---

## What you need to know

### Configuration comes from the environment

Week 5's rule, now load-bearing. The same image runs in development and production, and
**the only difference is the environment it is given.**

```python
class Settings(BaseModel):
    api_key: str
    model: str = "claude-sonnet-4-5"
    environment: str = "development"
    max_question_length: int = 500
```

Validate it at startup, not at first use. A service that starts happily and fails on the
first real request has wasted a deploy and a rollback.

**Fail loudly and say what to set:**

```python
raise RuntimeError(
    "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in."
)
```

### Never log a secret

```python
def redacted(settings):
    return {**settings.model_dump(), "api_key": mask(settings.api_key)}
```

Logging the config at startup is genuinely useful — it is how you find out that
production is pointing at the wrong model. Logging your key alongside it puts the key in
every log aggregator you use, forever. Redact once, in one place, and use that function
everywhere.

### Health checks

```python
@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION, "uptime_seconds": uptime()}
```

A platform calls this every few seconds to decide whether to send you traffic. So:

- **it must be cheap.** No model calls, no database queries. A health check that costs
  money is a health check that bankrupts you at 3am.
- **it must be honest.** If a dependency you need is missing, say so and return a 503.
  A service that reports healthy while broken is worse than one that reports nothing.

Two checks is a common split: `/health` for "am I running" (cheap, always) and
`/ready` for "can I actually serve" (checks dependencies).

### The start command

```
uvicorn app:app --host 0.0.0.0 --port $PORT
```

`0.0.0.0` rather than `127.0.0.1`, because in a container the request arrives from
outside it — this is the single most common reason a deploy "works locally" and returns
nothing in production.

`$PORT` from the environment, because the platform chooses it.

### A Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

Copy `requirements.txt` **before** the rest and install from it. Docker caches each
step, so this way a code change does not reinstall every dependency — it turns a
two-minute build into a five-second one, and it is the single most useful Docker fact
there is.

### `.env.example`

The names, no values:

```
ANTHROPIC_API_KEY=
MODEL=claude-sonnet-4-5
ENVIRONMENT=development
```

`.env` is gitignored; `.env.example` is committed. Somebody cloning your project now
knows exactly what they need without you handing over anything.

---

## Exercises

```bash
pytest week-11/day-2 -v
```

### 1. `config.py`

| Thing | Does |
|---|---|
| `Settings` | `api_key: str`, `model` (default `claude-sonnet-4-5`), `environment` (default `development`), `max_question_length` (1–5000, default 500), `request_timeout` (1–120, default 30) |
| `load_settings(env=None)` | build from a mapping, defaulting to the real environment |
| `mask(secret)` | `"sk-ant-abc123xyz"` → `"sk-a...3xyz"`; anything under 8 characters → `"****"` |
| `redacted(settings)` | the settings as a dict, with `api_key` masked |
| `is_production(settings)` | `True` when `environment` is `production` |

`load_settings` raises `RuntimeError` naming the variable when the key is missing or
empty, and rejects an `environment` that is not `development`, `staging` or `production`.

### 2. `health.py`

| Function | Returns |
|---|---|
| `uptime_seconds(started_at, now)` | whole seconds |
| `health_payload(started_at, now, version)` | `{"status": "ok", "version", "uptime_seconds"}` |
| `readiness(checks)` | `{"ready": bool, "checks": {...}, "failing": [...]}` |

`checks` is a dict of name to a zero-argument function returning a bool. A check that
**raises** counts as failing, not as a crash — a readiness probe that throws tells the
platform nothing.

### 3. `Dockerfile` and `.env.example`

Write both. The tests check that the Dockerfile installs requirements before copying the
code, binds `0.0.0.0`, and uses `$PORT`; and that `.env.example` names every variable and
contains no values.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 2" && git push
```

---

## Predict-then-run

Set `ANTHROPIC_API_KEY` to something, then print `redacted(load_settings())`.

Now imagine that line runs on every startup and the output goes to a log service your
whole company can read. Is there anything in it you would mind? That question, asked
once per new field, is most of what secret hygiene is.

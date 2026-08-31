# Week 11 — Concept fence

## Allowed

**Everything from Weeks 1–10**, plus:

- **FastAPI** — `FastAPI()`, `@app.get`, `@app.post`, Pydantic request and response
  models, `HTTPException`, `Depends`, `status`, `StreamingResponse`
- `fastapi.testclient.TestClient`
- `uvicorn` as the start command
- Structured logging with `logging` and `json`
- A request id, and a tracer you write yourself
- Your own eval gate — golden set, thresholds, a pass/fail
- A `Dockerfile` and a platform config file

## Not yet

Databases and ORMs · authentication beyond a shared API key · rate limiting middleware ·
Kubernetes, Terraform, autoscaling · CI/CD pipelines beyond one script · a frontend
beyond a single HTML page · OpenTelemetry — **you write the tracer**, then read about
LangSmith and recognise it

---

## Why you write the tracer

LangSmith, Langfuse and OpenTelemetry all do this properly and you should use one at
work. You write a small one first for the same reason you wrote the agent loop: so that
when you open LangSmith it looks like a nicer version of something you already
understand, rather than a magic dashboard.

It is about forty lines. Then read about the real ones and notice how much of it you
recognise.

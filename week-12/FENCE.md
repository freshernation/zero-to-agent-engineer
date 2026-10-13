# Week 12 — Concept fence

## Allowed

**Everything from Weeks 1–11**, plus:

- **FastAPI** — `FastAPI()`, `@app.get`, `@app.post`, Pydantic request and response
  models, `HTTPException`, `Depends`, `Header`, `status`, `StreamingResponse`
- `fastapi.testclient.TestClient`
- `uvicorn` as the start command
- Structured logging with `logging` and `json`
- A request id, and a tracer you write yourself
- One shared API key, checked with `secrets.compare_digest`
- Your own eval gate — golden set, thresholds, a pass/fail
- A judge checked against your own labels
- Fencing untrusted text, and an injection rate
- A `Dockerfile`
- One GitHub Actions workflow that runs the tests and the gate

## Not yet

Databases and ORMs · authentication beyond one shared API key · rate limiting middleware ·
Kubernetes, Terraform, autoscaling · CI/CD beyond that one workflow · a frontend
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

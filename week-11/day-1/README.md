# Day 1 — Behind an API

> **By the end of today** your agent answers HTTP requests instead of terminal input.

---

## Read / watch first

- [ ] [**FastAPI basics**](../../content/week-11/day-1/fastapi-basics.md) — 30 min · docs: [FastAPI — First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

---

## What you need to know

### The smallest service

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

```bash
uvicorn app:app --reload
```

`app:app` means *the object called `app` in the module called `app`*. Then
`http://127.0.0.1:8000/health` in a browser, and `/docs` for documentation FastAPI
generated from your code.

### Requests are Pydantic models

```python
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    k: int = Field(default=3, ge=1, le=10)

@app.post("/ask")
def ask(request: AskRequest):
    return {"answer": answer_question(request.question, request.k)}
```

Week 5's models, now doing three jobs at once: they validate the request, they document
the endpoint, and they reject bad input **before your code runs**. A request missing
`question` gets a 422 with a message naming the field, and you wrote no code for that.

`max_length=500` is not tidiness. Without it somebody posts a megabyte and you pay to
have a model read it.

### Responses are models too

```python
class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    refused: bool

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    ...
```

Declaring the response means it is documented, and that a field you forget to fill is an
error rather than a missing key somebody discovers in production.

### Status codes, deliberately

```python
from fastapi import HTTPException

if not question_is_answerable:
    raise HTTPException(status_code=404, detail="No documents matched")
```

Week 5 in reverse: then you read status codes, now you choose them. The same table
applies — 4xx is the caller's problem, 5xx is yours — and choosing correctly is what
lets a caller write sensible error handling.

### Dependency injection, again

```python
def get_agent():
    return AGENT

@app.post("/ask")
def ask(request: AskRequest, agent = Depends(get_agent)):
    ...
```

`Depends` is week 6's `client` parameter with framework support. The endpoint says what
it needs; something else decides what to give it — the real one in production, a fake
in tests. Same idea, third time.

### Testing it without a server

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.post("/ask", json={"question": "when are claims due"})
assert response.status_code == 200
```

No server, no port, no network. This is how every test today works.

---

## Exercises

```bash
pytest week-11/day-1 -v
```

### 1. `models.py`

| Model | Fields |
|---|---|
| `AskRequest` | `question: str` (1–500 chars), `k: int` (1–10, default 3) |
| `AskResponse` | `answer: str`, `sources: list[str]`, `refused: bool` |
| `HealthResponse` | `status: str`, `documents: int` |

### 2. `service.py`

| Endpoint | Does |
|---|---|
| `GET /health` | `{"status": "ok", "documents": n}` |
| `POST /ask` | answers a question |
| `GET /sources` | the document names |

Plus:

| Function | Returns |
|---|---|
| `create_app(answerer)` | the `FastAPI` app, using the answerer given to it |
| `default_answerer(question, k)` | a stub answer, so the app runs with nothing else |

`create_app` takes the answerer as an argument — dependency injection, third time. It is
what lets the tests run without a model.

Bad input gets a **422** and you write no code for it. An empty question is bad input.
`k` of 99 is bad input.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 1" && git push
```

---

## Predict-then-run

Start your service and open `http://127.0.0.1:8000/docs`.

Everything on that page came from your Pydantic models and type hints. Now change
`max_length` to 50 and reload.

That page is also the fastest way to show somebody your project works — worth knowing on
the day an interviewer asks you to demo something.

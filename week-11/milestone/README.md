# Project 3 — The Deployed Assistant

> A document assistant behind an API on the public internet, traced, guarded, and with
> an evaluation that blocks a bad deploy.

**This is the one that gets clicked.** Of your three projects it is the only one an
interviewer can try without cloning anything, and the link in your README needs to be
live on the day they read it.

---

## The files

| File | Holds |
|---|---|
| `pipeline.py` | `Assistant` — retrieval, generation, tracing |
| `app.py` | The FastAPI service |
| `evaluate.py` | The eval gate. Exits non-zero on failure. |
| `Dockerfile` · `.env.example` | Deployment |
| `PROJECT_README.md` | What a stranger reads |
| `DEPLOYMENT.md` | How you deployed it and what you would do differently |

Given to you: `chunking.py`, `loading.py`, `store.py`, `golden.py`, `tracer.py`,
`logs.py`, `guards.py`, and the corpus. Six weeks of your own answers, handed back so
this week is about assembling and shipping.

---

## `pipeline.py`

**`Assistant(corpus_dir, chunker=None, k=3, min_score=0.01)`**

| Member | Does |
|---|---|
| `build()` | load, chunk, index — returns itself |
| `chunk_count` | how many chunks |
| `sources` | the document names, sorted |
| `answer(client, question, request_id, clock)` | the full result |

`answer` returns:

```python
{
    "answer": str,
    "sources": list[str],
    "refused": bool,
    "request_id": str,
    "trace": dict,
    "duration_ms": int,
}
```

It must open a span for `retrieve` and one for `generate`, refuse **without calling the
model** when nothing scores, and cite its sources.

## `app.py`

| Endpoint | Does |
|---|---|
| `GET /health` | `{"status", "version", "uptime_seconds"}` — cheap |
| `GET /ready` | `{"ready", "checks", "failing"}` — checks the corpus is indexed |
| `GET /sources` | the document names |
| `POST /ask` | answers, with a `request_id` in the response |

Plus `create_app(assistant, client, settings)`, so the tests can build one without a
model or a key.

`POST /ask` must:

- reject a question over the configured length with a **413**
- return **429** when the daily budget is spent
- put the `request_id` in the response body **and** the `X-Request-ID` header
- never return a traceback

## `evaluate.py`

Runs the golden set, prints the summary, and **exits non-zero when the gate fails**.
That exit code is what a deploy pipeline reads.

```
$ python3 week-11/milestone/evaluate.py
hit_rate 0.850 >= 0.800 PASS
refusal_rate 0.150 <= 0.200 PASS
GATE PASSED
```

---

## `PROJECT_README.md`

The five sections from week 4, plus two that matter now:

| Section | What goes in it |
|---|---|
| `## What it is` | One sentence |
| `## Try it` | **The live URL**, and a `curl` that works |
| `## How it works` | Retrieval, then generation. Three or four sentences. |
| `## Running it yourself` | Commands that work from a fresh clone |
| `## How I know it works` | The eval numbers. This is the section that gets you asked good questions. |
| `## What I would do next` | Honest and brief |

## `DEPLOYMENT.md`

| Section | What goes in it |
|---|---|
| `## Where it runs` | Platform, and why that one |
| `## Configuration` | Every variable and what happens without it |
| `## What I would change` | For real traffic. Be specific. |

---

## Check it

```bash
pytest week-11/milestone -v
python3 week-11/milestone/evaluate.py
```

---

## Then deploy it, and check it as a stranger

- [ ] Open the live URL on your phone
- [ ] Paste the `curl` from your README into a fresh terminal
- [ ] Ask it something the corpus does not cover, and check it refuses
- [ ] Look at `/docs` and see whether it explains itself
- [ ] Ask somebody who is not on this course to try it, and watch without helping

That last one finds more than the other four together.

---

## Ship it

```bash
git add -A && git commit -m "project 3: deployed assistant" && git push
```

Pin it on your GitHub profile, next to Project 2.

---

## Friday

The defence starts with the live URL open on your instructor's machine. If it is down,
that is the defence.

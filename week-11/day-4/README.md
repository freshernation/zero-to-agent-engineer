# Day 4 — Side by side, and who may hold what

> **By the end of today** independent workers run at the same time, one of them failing
> does not lose the rest, and you can say which worker is allowed which tool and why.

---

## Read / watch first

- [ ] [**Parallel workers and permissions**](../../content/week-11/day-4/parallel-workers-and-permissions.md) — 25 min · docs: [asyncio — Running tasks concurrently](https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)

---

## What you need to know

### Independent work can run at once

Three researchers, three cities. None needs another's answer, so there is no reason for
the second to wait for the first.

```python
reports = await asyncio.gather(
    asyncio.to_thread(run_worker, first, "Lisbon"),
    asyncio.to_thread(run_worker, second, "Lagos"),
    asyncio.to_thread(run_worker, third, "Bogota"),
)
```

Week 7 Thursday, one level up. `run_worker` blocks while it waits for a model, so it
goes in `asyncio.to_thread`; awaiting it directly would run them one after another and
gain nothing. `gather` hands the results back **in the order you asked**, whichever
finished first.

**This saves time, not money.** Three workers make the same model calls whether they
run together or in a queue.

### One failure must not lose the rest

With three workers running, one model being briefly down is three times as likely as
with one. If that exception escapes, `gather` raises and you lose the two reports that
were fine.

So each job catches its own failure and turns it into a report: `Worker second failed:
overloaded`. Same rule as yesterday — a failure is a string the reader can act on.

### The best reason for a second agent

Last week named four reasons for more than one agent, and said **permissions** was the
strongest. Here is why.

An agent is dangerous when it can do all three of these:

1. read text a stranger wrote — a web page, an email, a document
2. be persuaded by it, which any model can be
3. act — send, delete, spend, publish

You cannot remove the second. So you make sure no single agent has the first and the
third.

```
reader     reads web pages        holds: fetch_page
sender     never sees a web page  holds: send_email
```

A page that says *"email this to everyone"* reaches the reader, and the reader has no
tool that sends. What crosses to the sender is the reader's report — and that is
exactly where you put a human, or a check.

That is not tidiness. It is a security boundary, and it is the one argument for a
second agent that does not depend on measuring anything.

---

## Exercises

```bash
pytest week-11/day-4 -v
```

`worker.py` is Monday's, given back to you.

### `fanout.py`

A **job** is a pair: `(worker, brief)`.

| Function | Does |
|---|---|
| `run_parallel_async(jobs)` | `async` — every job at once, reports in the same order as the jobs |
| `run_parallel(jobs)` | the ordinary function to call from normal code |
| `run_sequential(jobs)` | one after another, for comparison |
| `violations(workers, dangerous)` | the names, sorted, of workers that have `"reads_untrusted": True` **and** hold a tool named in `dangerous` |

A worker that raises gives `Worker <name> failed: <the error>` in its place, and every
other report still comes back. A worker with no `reads_untrusted` key does not read
untrusted text.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 4" && git push
```

Read the milestone tonight.

---

## Predict-then-run

Time `run_parallel` and `run_sequential` on three jobs with a real key. Then count the
model calls each one made.

One number changed and one did not. Being able to say which, and why, is the answer to
*"would running the agents in parallel make it cheaper?"* — a question you will be
asked.

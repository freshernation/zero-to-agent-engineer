# Day 4 — Doing several things at once, and debugging an agent

> **By the end of today** your agent runs several tool calls concurrently, and you can
> debug a loop that is misbehaving.

Short day. Tomorrow is Project 2.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on asyncio basics — 25 min]`

---

## What you need to know

### One response, several tools

A model can ask for more than one tool in a single reply:

```python
response.content    # [ToolUseBlock("city_info", ...), ToolUseBlock("city_info", ...)]
```

Your loop already handles this — you run every block and put every result in the same
user message. But you run them **one after another**, and each of these tools sleeps for
a tenth of a second waiting on something.

Three sequential calls: 0.3 seconds. Three concurrent: 0.1. That gap is why this matters.

### `async` in ninety seconds

```python
import asyncio

async def slow_thing(n):
    await asyncio.sleep(1)
    return n * 2

async def main():
    results = await asyncio.gather(slow_thing(1), slow_thing(2), slow_thing(3))
    return results          # [2, 4, 6] - after ONE second, not three

asyncio.run(main())
```

| | |
|---|---|
| `async def` | a function that can pause |
| `await` | pause here and let something else run |
| `asyncio.gather(...)` | start several, wait for all |
| `asyncio.run(...)` | the bridge from ordinary code into async |

**Async does not make anything faster.** It stops your program sitting idle while it
waits. Three tools that each wait on a network are perfect for it; three that each do
heavy arithmetic get no benefit at all — for those you would need processes, which is
a different topic and not one you need.

### Running a blocking tool from async code

Your tools are ordinary functions. Calling one directly inside `async def` blocks
everything, which defeats the point:

```python
result = await asyncio.to_thread(function, **arguments)
```

`to_thread` runs it on a separate thread and lets the loop carry on. It is the bridge
in the other direction, and it is exactly what you want for tools you did not write as
async.

### Where this actually pays

An agent asking for six web lookups at once. Sequentially that is six round trips of
waiting; concurrently it is one. This is the single most common real-world speedup in
agent code, and every framework does it for you — which is why it is worth doing once
by hand.

---

## Exercises

```bash
pytest week-07/day-4 -v
```

`toolkit.py` now has `slow_lookup(key)`, which sleeps for 0.1 seconds.

### 1. `parallel.py`

| Function | Returns |
|---|---|
| `run_tool_async(name, arguments)` | an `async` function returning the result string |
| `run_all_async(calls)` | an `async` function taking `[(id, name, arguments), ...]` and returning `[(id, result), ...]` **in the same order** |
| `run_all(calls)` | the ordinary function you call from normal code |
| `run_all_sequential(calls)` | the same, one after another — for comparison |

`run_all` on three `slow_lookup` calls must finish in **well under 0.3 seconds**. There
is a test that times it.

Order matters: `gather` preserves the order you passed things in, and the ids must line
up with the right results.

---

## Debugging, round seven

Three agent bugs. All three are caught by the fake client, which now enforces the same
rules the real API does.

| File | Should print |
|---|---|
| `broken_1.py` | `Answer: It is 391.` |
| `broken_2.py` | `Answer: Stopped after 3 steps without finishing.` |
| `broken_3.py` | `Results: ['4', '2']` |

- **`broken_1.py`** sends the tool result without resending what the model said.
- **`broken_2.py`** has a loop that ends without deciding anything.
- **`broken_3.py`** hard-codes the `tool_use_id`, so with two calls in flight the second
  answer claims to be the first.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 7 day 4" && git push
```

Tomorrow: Project 2, the defence, and the write-up.

---

## Predict-then-run

Take your `run_all` and give it three `calculate` calls instead of three
`slow_lookup` calls. Time it against `run_all_sequential`.

The difference is roughly nothing. Explain why — and you will have explained what
`async` is actually for, which is a question you will be asked in an interview.

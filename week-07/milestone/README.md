# Project 2 — The Agent

> A working agent. No framework. Plus a write-up explaining the loop in your own words.

This is the centrepiece of the course. Not because it is the most impressive thing you
will build — Project 3 is — but because almost nobody applying for these jobs can do it,
and the write-up proves you can.

---

## The files

| File | Holds |
|---|---|
| `tools.py` | The functions. Ordinary Python. No model anywhere. |
| `schemas.py` | The descriptions you send to the model |
| `agent.py` | `Agent` — the loop |
| `cli.py` | The program a person runs |
| `WRITEUP.md` | **The loop, explained by you** |

---

## `tools.py`

Four required, plus **at least one of your own**.

| Tool | Returns |
|---|---|
| `calculate(expression)` | the value; raises `ValueError("Unsafe expression")` for anything but digits, spaces and `+ - * / ( ) .` |
| `save_note(title, body)` | `"Saved note: Shopping"` — persists to `notes.json` |
| `list_notes()` | `"Shopping, Ideas"`, or `"No notes yet."` |
| `read_note(title)` | the body, or `"No note called Shopping."` |

The notes are the interesting part: they give the agent **state that survives between
tool calls**, so it can do genuinely multi-step work — *"work out 17 × 23 and save it as
a note called Maths"* needs two tools and the second depends on the first.

Your fifth tool is yours. Make it do something real and offline.

## `schemas.py`

`all_schemas()` returns one schema per tool. Every description must say what the tool
does **and when to use it**, in at least eight words. The description is the prompt.

## `agent.py`

**`Agent(client, max_iterations=6, max_repeats=2)`**

| Member | Does |
|---|---|
| `run(question)` | the final answer |
| `trace` | the record of the run |
| `stop_reason` | `"answered"`, `"cap"` or `"looping"` |
| `model_calls` | how many model calls |
| `last_answer` | the most recent answer |

Everything from Wednesday: unknown tools and failing tools return a string and the loop
carries on, results are truncated at 500 characters, a repeated call stops the run, and
the cap stops it otherwise.

## `cli.py`

```
> work out 17 * 23 and save it as a note called Maths
Saved note: Maths

> /trace
1. calculate({'expression': '17 * 23'}) -> 391
2. save_note({'title': 'Maths', 'body': '391'}) -> Saved note: Maths
3. answer: Saved note: Maths

> /quit
Bye.
```

| Command | Does |
|---|---|
| anything else | runs the agent, prints the answer |
| `/trace` | the last run's trace, one line per step |
| `/stop` | `Stop reason: answered` |
| `/quit` | prints `Bye.` and stops |

`/trace` before any question prints `No runs yet.`

---

## `WRITEUP.md` — the part that gets you hired

Five sections. Write it **after** the code works, from memory, without looking at your
own source.

| Section | What goes in it |
|---|---|
| `## The loop` | Every step, in order, in plain English. What happens on each pass and what makes it stop. |
| `## What a tool is` | The three parts: the schema, the model's request, your dispatch. Be explicit that the model never runs anything. |
| `## Why there is a cap` | What happens without one, and what it costs. |
| `## What went wrong` | A real failure you hit this week, and how you found it. Specific. Name the error. |
| `## What a framework would do` | What you would hand over next week, and what you would want to keep control of. |

At least 500 words in total. It is graded on whether the words are there and whether
certain ideas appear — `stop_reason`, `tool_use_id`, and the cap all have to be
mentioned, because a write-up that misses them was not written from understanding.

> **Say this out loud in an interview and watch what happens:** *"the model never
> executes anything — it emits JSON asking for a call, and my loop decides whether to
> make it."* Most candidates cannot.

---

## Check it

```bash
pytest week-07/milestone -v
```

Thirty-one tests. All against `FakeClient` — no key, no network, no cost.

Then run it for real if you have a key:

```bash
export ANTHROPIC_API_KEY=your-key-here
python3 week-07/milestone/cli.py --real
```

Ask it something that needs two tools. Watch `/trace`. That moment — seeing it decide,
act, and decide again on work you did not script — is the one worth having.

---

## Then make it good

- [ ] `tools.py` imports nothing model-related
- [ ] No framework anywhere. Check with `grep -ri langchain .`
- [ ] The cap is the first thing in the loop
- [ ] Every tool result is a string, always, including failures
- [ ] `WRITEUP.md` reads like you wrote it, because you did

---

## Ship it

```bash
git add -A && git commit -m "project 2: agent from scratch" && git push
```

Pin this repository on your GitHub profile. It is the one that will get read.

---

## Friday

Phase 1 opens with the paper test: **draw the loop, no laptop.** Then the mutate phase
adds a tool, and the debug phase is a seeded bug in the loop itself.

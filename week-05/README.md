# Week 5 — Talking to the internet

> **Destination**
> Call any HTTP API, check what came back is really what you expected, and keep working
> when it is not.

Python is over. From here everything is applied — and nothing you learned in weeks 1–4
gets left behind. An API response is a list of dicts. A retry is a `while` with a
counter. A validated model is a class with rules in `__init__`. You have all of it.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Fetch data over HTTP and read a status code |
| Tue | `day-2/` | Refuse to trust a response until it is validated |
| Wed | `day-3/` | Handle secrets, timeouts, retries — the unglamorous 80% |
| Thu | `day-4/` | Combine several endpoints into one answer |
| Fri | `milestone/` | Ship a report that merges three endpoints and survives all of them |

---

## What changes about how you work

**AI is now allowed to write code with you.** Weeks 1–4 were AI-off so that
decomposition and debugging would actually form. They have. From today the model is a
pair, not an author — and the rule that replaces the old one is simple:

> **You may not commit a line you could not have written, and could not explain on
> Friday.**

The defence does not get easier because the AI helped. It gets harder, because there is
more code to be responsible for.

Use `ai/editor.md` on everything. Keep using `ai/tutor.md` when you are stuck on an
idea rather than a keystroke.

---

## The idea this week is really about

**Anything outside your program is a liar.**

Not maliciously — it is just slow sometimes, down sometimes, and occasionally returns a
`null` where the documentation promised a string. Every network call has four possible
outcomes and your code has to have an answer for each:

| Outcome | Your answer |
|---|---|
| It worked | use the data |
| It failed politely (404, 500) | check the status code |
| It never answered | `timeout=` |
| It answered with rubbish | validate before you trust |

Most beginner code handles the first one. All four is the difference between a script
and a service, and it is what week 7's agent will depend on when a tool call goes wrong.

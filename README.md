# Zero to Agent Engineer

Thirteen weeks from your first line of Python to a deployed, evaluated agent system.

You are here because you want a job. Everything in this repo is aimed at that and
nothing else. If something looks missing, it was cut on purpose — see `CUT_LIST.md`.

---

## The three rules

**1. The twenty-minute rule.**
Stuck? Struggle alone for twenty minutes. Then open the **tutor** (`ai/tutor.md`) —
never a plain chat, never "write this for me". Then, and only then, bring it to the
live hour. Log every stuck event in `logs/stuck-log.md`.

**2. You write every line for the first four weeks.**
Weeks 1–4 are AI-off for writing code. The AI is a tutor, not an author. Not a moral
position — decomposition and debugging are the two skills that get you hired, and they
are exactly the two the model will quietly do for you if you let it.

From week 5 the AI may write code with you, and the rule that replaces it is:
**you may not commit a line you could not have written and cannot explain on Friday.**

**3. Nothing counts until the tests pass and it's pushed.**
"It works on my machine" is not a milestone.

---

## Daily rhythm

| | |
|---|---|
| **Live hour** | One hour with your instructor, five days a week |
| **Independent** | Four or more hours a day — where the learning actually happens |
| **Friday** | No new content. Defend, ship, retro. |

---

## The thirteen weeks

| Week | | Milestone |
|---|---|---|
| 1 | Code is not magic | A CLI bill-splitter |
| 2 | Many things at once | A sales report from raw records |
| 3 | Pieces, storage, failure | A two-file expense tracker with JSON persistence |
| 4 | Objects, tests, an audience | **Project 1** — tested, documented, on GitHub |
| 5 | Talking to the internet | A report merging three API endpoints |
| 6 | Talking to a model | A streaming assistant with memory and a cost counter |
| 7 | **Build the agent** | **Project 2** — an agent with no framework, and the write-up |
| 8 | Frameworks, on your terms | Both agents side by side, plus the comparison |
| 9 | Retrieval, and proving it | RAG with a measured before-and-after |
| 10 | Multi-agent, and its cost | The same task two ways, plus a recommendation |
| 11 | Put it where people can reach it | **Project 3** — deployed, traced, evaluated |
| 12 | The interview is the deliverable | Ten recorded mocks, scored |
| 13 | Buffer, and pressure | Applications out, and the plan |

Week 7 is the keystone. Week 12 is the one people underestimate.

---

## How to work

```bash
source .venv/bin/activate          # every session

pytest week-01/day-1 -v            # one day
pytest week-01 -v                  # one week
```

Tests are the grader. A green test means "this behaves correctly", not "this is good
code" — the **editor** (`ai/editor.md`) judges the second thing, and your instructor
judges both on Friday.

**1,497 tests** across the course. Every one of them fails before you write anything.

---

## Map

| Path | What it is |
|---|---|
| `SETUP.md` | Day zero. Do this before anything else. |
| `week-01/` … `week-13/` | One folder per week: four days, a milestone, a fence, a defence |
| [`content/`](content/README.md) | The reading for every day — 66 articles, each opening with the official docs |
| `ai/` | Your four AI roles — tutor, editor, interviewer, defend |
| `logs/stuck-log.md` | Every time you get stuck. Non-negotiable. |
| `logs/signal-log.md` | Your daily five numbers. Two minutes at end of day. |

Both logs are **read by your instructor before every live hour**. They are not
busywork and they are not marked — an honest amber gets you help, and a blank log
gets you asked why it is blank.
| `CUT_LIST.md` | What this course deliberately does not teach, and why |

Each week has a `FENCE.md` listing what you have learned and what you have not. Paste
both lists into any AI role before you use it — it is what stops the model teaching you
something three weeks early and making your toolkit feel inadequate.

---

## The three projects

Everything builds towards these, because the project deep-dive is the interview round
that decides it.

| | Week | Proves |
|---|---|---|
| **Expense Tracker** | 4 | you can write Python, not assemble it |
| **Agent From Scratch** | 7 | you understand agents rather than importing them |
| **Deployed Assistant** | 11 | you can ship — the claim that closes offers |

---

## What this week is not about

Elegance. Speed. "Pythonic" style. Anything in the "not yet" column of this week's
`FENCE.md`.

You will write clumsy code and that is correct. Clumsy code you understand completely
beats elegant code you copied, and it is not close — the second kind collapses the
moment somebody asks you a question about it.

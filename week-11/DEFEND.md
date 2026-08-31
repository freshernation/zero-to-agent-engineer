# Week 11 — Friday defence

**Start with the live URL open on your machine, before anything else.** If it is down,
that is the defence — spend the hour getting it up, and say plainly that a portfolio
project which is not reachable is not a portfolio project.

---

## Phase 0 — The stranger test (5 min)

Open their `PROJECT_README.md` and follow it **exactly**, on your machine, out loud.
Click the link. Paste the `curl`. Do not fill in any gap for them.

Whatever breaks is the most valuable thing you find today, because an interviewer will
do this and will not tell you what went wrong — they will just close the tab.

## Phase 1 — Explain (7 min)

1. *"A user says it gave a wrong answer at 3pm yesterday. Find that request."* — the
   question the whole week was for. Looking for: the request id, the log line, the trace,
   and which span was slow.
2. *"Your `/health` is called every five seconds. What does it cost?"* — nothing. Then:
   *"and what would it cost if you had put the search in it?"*
3. *"Why is the refusal check before the model call rather than after?"*
4. *"Your eval gate exits non-zero. Who reads that?"*
5. *"What is in your logs that you would mind the whole company seeing?"* — should be
   nothing, and they should be able to point at the redaction.

## Phase 2 — Mutate (8 min)

### Mutation A — *"Add a `/ask/stream` endpoint that streams the answer."*

Name the pieces before typing: `StreamingResponse`, the model's streaming call from week
6, and — the interesting part — **what happens to the trace and the log line**, which
currently happen after the answer is complete. There is no clean answer; watching them
notice the problem is the point.

### Mutation B — *"Traffic goes up ten times. What breaks first?"*

Discussion. Looking for: the daily budget, then the per-process index being rebuilt on
every restart, then the lack of per-caller rate limiting. A student who says "I would add
caching" without saying what they would cache has not thought about it.

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `/health` returns the wrong version | Reading a diff |
| Medium | bind `127.0.0.1` in the Dockerfile | Works locally, dead in the container |
| Medium | the budget records a refused spend | Only the third request over the limit shows it |
| Hard | remove the redaction from one log call | Nothing fails. The key is in the logs. |
| Nasty | the eval gate compares `refusal_rate >=` instead of `<=` | The gate passes a system that refuses everything |

The **Nasty** one is the best of the course: a deploy gate that waves through the exact
failure it exists to catch, and every test still green.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Stranger** | Works from a cold read, first time | One small gap | Link dead, or commands do not run |
| **Explain** | Traces a request end to end | Knows where to look | Cannot find one request |
| **Mutate** | Spots the tracing problem in streaming | Builds the endpoint | Cannot see past the code |
| **Debug** | Suspects the measurement | Finds it | Guesses |

**A dead link is a fail regardless of the rest.**

---

## Retro (10 min)

1. *"Which of the three projects would you show first, and why?"*
2. *"What did you cut to get this deployed, and was it the right cut?"*
3. *"What did I explain badly?"*

---

## Instructor: this is the last build week

Say it plainly:

> **You are done building. Everything from here is about being hired.** Next week is
> interviews — ten of them, recorded, scored. The week after is applications. The code
> stops changing and the pressure goes up.

Then, before they leave, check three things yourself and make a list:

1. Both GitHub profiles have all three projects pinned
2. Every README has a working link and commands that run
3. Both live URLs are up

Whatever is not true on that list is Monday's first hour. Week 12 is much less useful if
the artifacts it points at are broken.

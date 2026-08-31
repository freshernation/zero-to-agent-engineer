# Day 2 — Applications

> **By the end of today** ten applications are out and you can tell which channel is
> working.

---

## What you need to know

### Volume, then learning

Ten good applications beat two perfect ones, for the same reason the tenth mock was
better than the first. You improve by doing it, and you cannot improve a thing you do
twice.

But volume without a record teaches nothing. Track them from the first one, because the
question that matters — *which channel actually converts?* — cannot be answered
retrospectively from memory.

### The channels, roughly in order of how well they work

| Channel | Reality |
|---|---|
| **Referral** | By far the best. A name attached to your application changes who reads it. |
| **Direct** | Applying on the company's own site. Slower, but it reaches a human. |
| **Board** | Volume play. Low response rate, and that is fine if you treat it as volume. |
| **Agency** | Variable. Some are excellent; most will send your CV everywhere without asking. |

Most people spend all their effort on the channel that converts worst, because it is the
one that does not involve talking to anybody. Tomorrow is about the one that does.

### The application itself

**Tailor one paragraph, not the whole thing.** Your résumé is already good. What changes
per application is a short note saying why *this* company — one specific thing, from
their job posting or their engineering blog.

**Link the deployed project.** It is the only one they can try without cloning
anything, and a link that works is worth more than a paragraph of description.

**Do not apologise for the career change.** Nobody is owed an explanation. "Career
changer with three shipped projects, one deployed" is a fact, not a confession. The
phrase to avoid entirely is "although I don't have a computer science degree".

### Follow up once

If nothing has happened after ten working days, one short message. Once. Then let it go
and put the effort into the next application — chasing is not the same as applying, and
it feels productive while not being.

---

## Exercises

```bash
pytest week-13/day-2 -v
```

### 1. `applications.py`

| Thing | Is |
|---|---|
| `APPLICATIONS` | at least ten, each with `company`, `role`, `source`, `applied` (ISO date), `status` |
| `count_by_status(apps)` | `{status: count}` |
| `response_rate(apps)` | fraction that got past `applied`, to 2dp |
| `by_source(apps)` | `{source: count}` |
| `response_rate_by_source(apps)` | `{source: rate}` |
| `best_source(apps)` | the source with the highest response rate; ties go alphabetically |
| `needs_follow_up(apps, today, days=10)` | still `applied` after `days` working days — company names, in order |

`source` is one of `referral`, `direct`, `board`, `agency`. `status` is one of
`applied`, `screening`, `interview`, `offer`, `rejected`, `ghosted`.

"Got past applied" means anything except `applied` and `ghosted`.

### 2. `APPLICATIONS.md`

The same list in readable form, plus a `## What I am learning` section — at least 100
words on what the numbers are telling you after ten.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 13 day 2" && git push
```

Tomorrow: the channel that actually works. Bring a list of everyone you know who works
anywhere near software. It is longer than you think.

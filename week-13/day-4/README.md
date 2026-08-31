# Day 4 — Keeping the repo warm

> **By the end of today** Project 3 has one shipped improvement and a changelog entry.

---

## What you need to know

### A frozen repository tells a story

An interviewer looks at the commit graph. A repository whose last commit is the day a
course ended says *"this was homework"*. One with a commit from last Tuesday says
*"this is something I work on"*.

The difference costs about an hour a week and it is the cheapest signal you can send.

### One improvement, actually shipped

Not a refactor nobody can see. Something a user would notice, small enough to finish
today, and deployed by the end of it.

Good candidates, in rough order of value:

| Improvement | Why |
|---|---|
| Whatever your eval said was weakest | It is measured, so you can prove it worked |
| The thing somebody told you was confusing | Outreach yesterday probably gave you one |
| A failure mode you know about and have not handled | Shows you were honest about it |
| Better first-screen copy | Most visitors leave from there |

Bad candidates: a rewrite, a new framework, a fourth project.

### Prove it worked

Run the eval gate before and after. If the change was meant to improve retrieval and the
number did not move, that is worth knowing and worth writing down — a changelog entry
that says *"tried X, hit rate unchanged, reverted"* is more impressive than one that
claims an improvement with nothing behind it.

### The changelog

One entry per change, newest first, in a form a stranger can read:

```markdown
## 2026-01-22

- Chunk overlap raised from one sentence to two. Hit rate 0.850 -> 0.900 on the
  twenty-question golden set. The two questions it fixed were both ones where the
  answer sat across a paragraph break.
```

What changed, what it did to the number, and why. Three sentences.

---

## Exercises

### `CHANGELOG.md`

At least one entry, dated, with:

- what changed
- what it did to a measurable number — **including "nothing"**
- why, in one sentence

### `SHIPPED.md`

| Section | What goes in it |
|---|---|
| `## What I changed` | And why that one |
| `## Before and after` | The numbers, both of them |
| `## What it cost` | Time, and anything it made worse |
| `## The habit` | What you are committing to weekly, and when |

```bash
pytest week-13/day-4 -v
```

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 13 day 4" && git push
```

Then push the improvement to the live service and check it on your phone.

Tomorrow is a full-length mock, unannounced in content, at real interview difficulty.

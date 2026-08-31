# Week 2 — Many things at once

> **Destination**
> Hold a collection of things, do something to every one of them, and summarise the
> result.

Last week every program handled one value at a time. That is not what software does.
This week your programs start handling *thirty* things, then a hundred, with the same
amount of code — and that is the leap that makes programming worth doing.

Still **AI-off for writing code.** The tutor diagnoses; you type.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Keep many values in one place and reach any of them |
| Tue | `day-2/` | Do something to every item without writing it out ten times |
| Wed | `day-3/` | Label your data instead of counting positions |
| Thu | `day-4/` | Rank, deduplicate, and debug collections |
| Fri | `milestone/` | Ship the sales report, then defend it |

---

## What last week bought you

Everything you learned in week 1 is still the whole toolkit — `if`, arithmetic,
f-strings, `input()`. You are not replacing it. You are adding a way to point at
many values at once, and a way to repeat work.

If week 1 still feels shaky, say so on Monday rather than pushing through. Loops
built on a wobbly understanding of variables produce bugs that look like magic, and
this is the last week where going back is cheap.

---

## Milestone

A sales report generator: ten records in, a formatted summary with totals, an average,
and a ranking out. Spec in `milestone/README.md`.

---

## A warning about this week specifically

Week 2 is where beginners most often start copying. Loops over dicts *look* hard, the
shapes are unfamiliar, and there is a working example of everything on the internet.

The tell is Friday. Someone who copied can run their report and cannot add a column to
it. The mutation phase of the defence exists precisely to find this, in the week where
it is still easy to fix.

# Week 1 — Code is not magic

> **Destination**
> Write, save, and run a Python program that reacts to what a person types — and get it
> onto GitHub.

By Friday you will have written maybe two hundred lines of code, every one of them
yourself. That is the point. Weeks 1–4 are **AI-off for writing code**: the model
tutors you (`ai/tutor.md`) and never authors for you.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Run a file and make the computer print exactly what you meant |
| Tue | `day-2/` | Store values, do arithmetic on them, and read what a person types |
| Wed | `day-3/` | Make the program choose between paths |
| Thu | `day-4/` | Read a traceback and fix code you did not write |
| Fri | `milestone/` | Ship the bill-splitter, then defend it |

Each day folder has its own `README.md`. Start there, every time.

---

## How a day goes

1. **Read** the day's README. All of it, before writing anything.
2. **Predict, then run.** Before you run any file, say out loud what you think it will
   print. Being wrong here is worth more than being right.
3. **Write** the exercises. In order — they build.
4. **Test** with `pytest week-01/day-N -v`. Green means correct behaviour, nothing more.
5. **Log** anything that stuck you in `logs/stuck-log.md`, and your five numbers in
   `logs/signal-log.md`.
6. **Commit and push.** Every day. `git add -A && git commit -m "day 1" && git push`

Four hours a day, five days. If you finish the exercises in two, go back and make the
code better — the **editor** (`ai/editor.md`) will find you plenty to do.

---

## Milestone

A working bill-splitter. Spec in `milestone/README.md`. It must pass its tests **and**
survive Friday's defence, which is a different and harder bar.

---

## What this week is not about

Elegance. Speed. "Pythonic" style. Anything in the "not yet" column of `FENCE.md`.

You will write clumsy code this week and that is correct. Clumsy code you understand
completely beats elegant code you copied, and it is not close — the second kind
collapses the moment someone asks you a question about it.

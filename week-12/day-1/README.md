# Day 1 — The artifacts

> **By the end of today** your résumé and GitHub survive a ninety-second read, and you
> can tell each project's story in two minutes.

---

## Read / watch first

- [ ] [**Résumés for career changers**](../../content/week-12/day-1/resumes-for-career-changers.md) — 20 min · source: your own project READMEs, and [GitHub — About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

---

## What you need to know

### Ninety seconds

That is roughly how long a first read gets. Not because people are lazy — because there
are two hundred of you and one of them.

So the top third of page one does the work. For a career changer that means **projects
above education**, always. Your three projects are the evidence; a bootcamp or a degree
in something else is context.

### One line per project, and it says what it does

| Weak | Strong |
|---|---|
| "Built an AI agent using Python and LangChain" | "Agent that answers questions from a document set, hand-written tool loop then ported to LangGraph — 0.85 retrieval hit rate, deployed" |

The second one has a number, a decision, and something checkable in it. The first could
have been written by somebody who watched a tutorial, and the reader knows that.

### The GitHub profile

The first three pinned repositories are your portfolio. Everything else is noise.

For each one:

- a README that opens with **what it is**, in one sentence
- commands that work from a cold clone
- a live link if there is one
- commits that read like somebody building something, not one commit called "stuff"

An interviewer who opens a repository and cannot tell what it does in fifteen seconds
closes it. That is not unfair; it is the same fifteen seconds you would give.

### The project story

Two minutes, four beats, in this order:

1. **What it does** — one sentence, no technology
2. **The interesting decision** — and the alternative you rejected
3. **What went wrong** — a specific bug, named
4. **What you would do next** — one thing, with a reason

Beat 3 is the one people skip and the one that lands. Everybody's project worked in the
demo; only somebody who built it can tell you exactly how it broke.

**Rehearse the story, not the words.** A memorised paragraph collapses at the first
interruption, and you will be interrupted.

---

## Exercises

```bash
pytest week-12/day-1 -v
```

### 1. `story.py`

| Function | Returns |
|---|---|
| `PROJECTS` | your three, each with `name`, `one_line`, `decision`, `alternative`, `broke`, `next_step` |
| `one_liner(project)` | the résumé line |
| `story(project)` | the four beats as a numbered string |
| `check(project)` | `{"ok": bool, "problems": [...]}` |

`check` complains when: the one-liner has no number in it, any beat is under eight
words, or `broke` contains no specific error or symptom.

### 2. `RESUME.md`

Your actual résumé, in Markdown. Sections: `## Projects` (three, one line each with a
number), `## Skills`, `## Experience`, `## Education`.

**Projects first.** There is a test for the order, and it is the single most important
formatting decision on the page.

### 3. `GITHUB.md`

An audit of your own profile. For each of the three: the repo name, whether it is
pinned, whether the README opens with what it is, whether the commands work from a cold
clone, and the live link if there is one.

Fill it in by **actually checking**, not from memory.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 12 day 1" && git push
```

---

## Predict-then-run

Hand your résumé to someone who is not on this course. Give them ninety seconds. Take it
back and ask what you build.

Whatever they say is what your résumé says, regardless of what is written on it.

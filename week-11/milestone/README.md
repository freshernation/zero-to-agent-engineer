# Week 11 Milestone — One Agent or a Team, Measured

> The same six questions answered by one agent and by a team, with the pass rate and
> the cost of each, and a recommendation you can defend.

Last week you estimated. This week the numbers are real, and they are yours.

---

## The files

| File | Holds |
|---|---|
| `designs.py` | The single agent, and the team |
| `compare.py` | Scoring, the two summaries, and the comparison |
| `REPORT.md` | **The deliverable** |

Given to you: `worker.py` and `team.py` — your own answers from Monday and Wednesday —
and `tasks.py`, six questions with the figure a correct answer must contain.

---

## `designs.py`

| Function | Returns |
|---|---|
| `run_single(client, question)` | `run_agent`'s result, for **one** agent holding both tools |
| `build_team(researcher_client, analyst_client)` | `[researcher, analyst]` |
| `run_as_team(orchestrator_client, question, workers)` | `run_team`'s result |

The researcher holds `lookup_population` and nothing else. The analyst holds
`calculate` and nothing else. If either could do the other's job you would have built
one agent twice.

Each worker needs a description of ten words or more — it is all the orchestrator has
to choose from — and a system prompt of its own.

## `compare.py`

| Function | Returns |
|---|---|
| `passed(text, expected)` | `True` when the expected figure is in the text, ignoring commas and capitals |
| `summarise(runs)` | `{"tasks", "pass_rate", "calls_per_task"}` from `[{"passed", "model_calls"}, ...]` |
| `compare(single, team)` | `{"quality_gain", "cost_ratio"}` |
| `recommend(comparison, min_gain=0.10)` | `"team"` only when the quality gain is at least `min_gain`; otherwise `"single-agent"` |

`pass_rate` and `quality_gain` to 2 decimal places, `calls_per_task` and `cost_ratio`
to 1. The quality gain is the team's pass rate minus the single agent's. The cost ratio
is the team's calls per task divided by the single agent's.

**The dearer design has to buy something you can measure.** That is the whole of
`recommend`.

---

## Then run it for real

The tests use scripted models. Your report cannot.

With a key, run both designs over all six tasks, **three times each**, and record for
every run whether it passed and how many model calls it made. For the team, keep the
delegations too — you will need the briefs.

Six tasks is a small set. One task is 17 points of pass rate. Say so in the report, and
do not claim a difference smaller than that.

## `REPORT.md`

| Section | What goes in it |
|---|---|
| `## What I built` | The two designs, concretely. Who holds which tool. |
| `## The numbers` | Pass rate and calls per task for each, the gain and the ratio, and how many runs they came from. |
| `## What crossed the handoff` | The briefs your orchestrator wrote, what you changed, and one thing a worker saw that never came back. |
| `## Where a team would win` | Be fair to it. Name the task, and the reason. |
| `## My recommendation` | And the measurement that would change it. |

At least 350 words, at least four numbers, and it must talk about the **brief**.

> *"One agent, and here is the number that says so"* is a complete and senior answer.
> So is *"a team, because the agent that reads the web must not hold the tool that
> sends"*. What is not an answer is *"a team, because it is more scalable"*.

---

## Check it

```bash
pytest week-11/milestone -v
```

---

## Ship it

```bash
git add -A && git commit -m "week 11 milestone: one agent or a team" && git push
```

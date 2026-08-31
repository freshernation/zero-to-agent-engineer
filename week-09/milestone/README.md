# Week 9 Milestone — RAG, Measured

> A question-answering system over the corpus, and a measured before-and-after that
> proves one change made it better.

The number is the deliverable. The system is how you get one.

---

## The files

| File | Holds |
|---|---|
| `pipeline.py` | `RagSystem` — build, search, answer |
| `harness.py` | The evaluation: hit rate, misses, comparisons |
| `report.py` | The program: runs the evaluation and prints the table |
| `FINDINGS.md` | **What you measured, what changed, and what still fails** |

Given to you: `chunking.py`, `loading.py`, `store.py`, `golden.py` — this week's earlier
answers, so the milestone is about assembling and measuring rather than rewriting.

---

## `pipeline.py`

**`RagSystem(chunker, k=3, min_score=0.01)`**

| Member | Does |
|---|---|
| `build(corpus_dir)` | load, chunk, index — returns itself so it can be chained |
| `search(question)` | the top `k` results |
| `answer(client, question)` | `{"answer", "sources", "results", "refused"}` |
| `chunk_count` | how many chunks are indexed |

`answer` must **decline without calling the model** when the top score is below
`min_score`, and set `refused` to `True`. It must cite sources and use the exact refusal
sentence:

```
I don't know based on the documents I have.
```

## `harness.py`

| Function | Returns |
|---|---|
| `evaluate(system, golden)` | `{"hit_rate", "hits", "total", "misses"}` |
| `compare(corpus_dir, golden, configurations)` | `{name: report}` for a dict of named `RagSystem`s |
| `format_comparison(reports)` | a table, one line per configuration |
| `improvement(reports, baseline, candidate)` | the difference in hit rate, rounded to 3dp |

`format_comparison` output:

```
fixed-200          0.650   13/20
sentence-400-o1    0.850   17/20
```

Name left-aligned in 18, rate to 3 decimals, then hits out of total.

## `report.py`

Running it prints the comparison table, the improvement, and the questions still missed:

```
$ python3 week-09/milestone/report.py
RETRIEVAL EVALUATION
==================================================
fixed-200          0.650   13/20
fixed-400          0.800   16/20
sentence-400-o1    0.850   17/20
==================================================
Improvement: +0.200 (fixed-200 -> sentence-400-o1)

Still missed by sentence-400-o1:
  - I accidentally pushed a password to git, what now
  ...
```

---

## `FINDINGS.md` — the deliverable

| Section | What goes in it |
|---|---|
| `## What I measured` | The metric, why hit rate at k and not something else, and the size of the golden set. |
| `## The change` | One variable. Both numbers. What you expected and whether you were right. |
| `## What still fails` | List the remaining misses and say **why**. Be specific about the mechanism. |
| `## What I would do next` | With a budget for exactly one improvement, what and why. |

At least 350 words. It must contain **at least two numbers** and mention **retrieval
miss**.

> **This document is the answer to "how did you know your retrieval was any good?"**
> Have it ready. Most candidates have nothing at all.

---

## Check it

```bash
pytest week-09/milestone -v
python3 week-09/milestone/report.py
```

---

## Then make it good

- [ ] `pipeline.py` and `harness.py` contain no `print()`
- [ ] The chunker is passed in, never hard-coded
- [ ] The refusal happens before the model call, not after
- [ ] Every configuration in the comparison is scored on the **same** golden set
- [ ] `FINDINGS.md` has real numbers from your own run

---

## Ship it

```bash
git add -A && git commit -m "week 9 milestone: RAG, measured" && git push
```

---

## Friday

The defence is mostly about the numbers, and about the three questions your system
still gets wrong.

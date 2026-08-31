# Day 4 — Gating the deploy

> **By the end of today** a bad change cannot reach production, and a runaway request
> cannot empty your account.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on LLM evaluation and guardrails — 25 min]`

---

## What you need to know

### Week 9's harness, wired to the deploy

You already measure retrieval. The step nobody takes is making that measurement
**block** something:

```
run the golden set  ->  compare to thresholds  ->  pass: deploy.  fail: do not.
```

A number nobody acts on is a number nobody looks at. A number that stops a deploy gets
looked at every single time.

### Judging the answer, not just the retrieval

Hit rate says the right passage was fetched. It says nothing about whether the answer
built from it was any good. For that you need a judge, and the usual judge is another
model call:

```
You are grading an answer against a reference.

Score 1 to 5:
5 - correct and complete
3 - correct but missing something important
1 - wrong, or contradicts the reference

Return only JSON: {"score": <1-5>, "reason": "<one sentence>"}
```

Week 6's structured output, doing a new job.

**Be honest about what this is.** An LLM judge is cheap, fast, and agrees with a human
often but not always. It is good for catching a regression between two versions of your
own system. It is bad as a claim about absolute quality. The way to use it is
comparatively — *"version B scored worse than version A on the same questions"* — which
is what a deploy gate needs anyway.

### Thresholds, decided in advance

```python
THRESHOLDS = {"hit_rate": 0.80, "mean_score": 3.5, "refusal_rate": 0.20}
```

Set them **before** you run, or you will find yourself lowering one to get a deploy out.
Everybody does it once.

The refusal rate is worth including in both directions: a system that never refuses is
making things up, and one that always refuses is useless. A gate that only measures
success misses half of what can go wrong.

### Guardrails

Evaluation stops bad changes. Guardrails stop bad **requests**:

| Guard | Stops |
|---|---|
| Question length | somebody posting a megabyte you pay to read |
| Cost budget per request | a runaway agent loop |
| Cost budget per day | a runaway agent loop that restarts |
| Iteration cap | week 7's, still earning its place |

The daily budget is the one people skip and then learn about from an invoice. Track what
you spend, refuse when you are over, and log the refusal loudly — a service that silently
stops answering is worse than one that says why.

---

## Exercises

```bash
pytest week-11/day-4 -v
```

### 1. `judge.py`

| Thing | Does |
|---|---|
| `JUDGE_SYSTEM` | the rubric: 1–5, what each end means, JSON only |
| `judge(client, question, answer, reference)` | `{"score": int, "reason": str}` |
| `mean_score(judgements)` | to 2dp, `0.0` for none |

An unparseable or out-of-range judgement scores **0** with a reason saying so. A judge
that crashes on its own bad output is not a judge.

### 2. `gate.py`

| Function | Returns |
|---|---|
| `THRESHOLDS` | `hit_rate` 0.80, `mean_score` 3.5, `refusal_rate` 0.20 |
| `check(report, thresholds)` | `{"passed": bool, "failures": [...]}` |
| `summarise(report, thresholds)` | one line per metric: `"hit_rate 0.850 >= 0.800 PASS"` |
| `exit_code(result)` | `0` when it passed, `1` when it did not |

`hit_rate` and `mean_score` must be **at or above** their thresholds; `refusal_rate` must
be **at or below** its own. Getting that direction right is the whole function.

### 3. `guards.py`

| Thing | Does |
|---|---|
| `check_question(text, max_chars)` | `(True, "")` or `(False, "Question is too long (612 > 500)")` |
| `Budget(limit)` | `spend(amount)`, `remaining`, `spent`, `would_exceed(amount)`, `reset()` |

`spend` past the limit raises `BudgetExceeded` and **does not record the spend** — a
budget that goes further over every time it is asked is not a budget.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 11 day 4" && git push
```

Read the milestone tonight. Tomorrow is Project 3.

---

## Predict-then-run

Set your thresholds, run the gate, and watch it pass. Now lower `hit_rate` in your own
system until the gate fails.

Then notice the feeling of wanting to lower the threshold instead of fixing the system.
That feeling is why the thresholds get set first, and naming it now is worth more than
any rule.

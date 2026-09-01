# Day 4 — Measuring it

> **By the end of today** you can put a number on your retrieval, change something, and
> prove the number moved.

This is the week. Everything before today was building the thing; today is the part
almost nobody does, and it is the part that gets discussed in interviews.

---

## Read / watch first

- [ ] [**Evaluating retrieval**](../../content/week-09/day-4/evaluating-retrieval.md) — 25 min · docs: [Create strong empirical evaluations](https://docs.claude.com/en/docs/test-and-evaluate/develop-tests)

---

## What you need to know

### The golden set

A list of questions, each with the answer you know is in the corpus:

```python
("when must expense claims be submitted", "fifth of the following month")
```

`golden.py` has twenty of them, given to you. **Writing one of these for your own
corpus is the highest-value afternoon you can spend on a RAG system**, and it is
unglamorous enough that most teams never do it.

Twenty is enough to be useful. A hundred is better. Zero — which is where most projects
are — means every claim about quality is a feeling.

### Hit rate at k

> Of the questions, in what fraction did the right passage appear in the top `k`?

```python
def hit_rate(store, golden, k=3):
    hits = 0
    for question, expected in golden:
        results = store.search(question, k=k)
        if any(expected.lower() in r["chunk"]["text"].lower() for r in results):
            hits += 1
    return round(hits / len(golden), 3)
```

Fifteen lines, and it turns "the retrieval seems fine" into `0.65`. It is the single
most useful number in a RAG system because **it separates the two halves**: if the
passage was never retrieved, no prompt engineering can save the answer.

### Why this metric and not another

You will meet precision, recall, MRR and NDCG. They are all worth knowing, and hit rate
at k is the right one to start with because it maps exactly onto what your system does:
it fetches `k` chunks and puts them in a prompt. If the answer is in those `k`, the
generation step has a chance. If not, it does not.

**Measure the thing your system actually does.** A sophisticated metric measuring
something else is worse than a crude one measuring the right thing.

### Changing one thing at a time

```
fixed 200, no overlap      hit@3 = 0.65
sentence 400, overlap 1    hit@3 = 0.85
```

That is a real result from this corpus, and it is what a comparison looks like: one
variable, both numbers, same questions.

Change the chunking **and** `k` at once and you have learned nothing about either. This
is the same discipline as week 1's debugging rule — change one thing — and it is the
same reason.

### Reading the failures

The number tells you *whether*. The failure list tells you *why*, and it is where the
work actually is:

```
missed: I accidentally pushed a password to git, what now
missed: what happens if I ignore the pager
```

Look at those two. Neither shares many words with the passage that answers it — the
document says "rotate the credential", the question says "pushed a password". **No
amount of chunking fixes that**, because TF-IDF matches words and the words are not
shared.

That is the honest limit of what you are using, and finding it yourself is worth far
more than being told. It is also precisely the gap a neural embedding closes, which
makes it the best possible argument for why they exist.

---

## Exercises

```bash
pytest week-09/day-4 -v
```

`golden.py`, `chunking.py`, `loading.py` and `store.py` are all given.

### 1. `evaluate.py`

| Function | Returns |
|---|---|
| `is_hit(results, expected)` | `True` if any retrieved chunk contains the phrase, ignoring case |
| `hit_rate(store, golden, k=3)` | the fraction, rounded to 3dp |
| `misses(store, golden, k=3)` | the questions that failed, in order |
| `evaluate(store, golden, k=3)` | `{"hit_rate", "hits", "total", "misses"}` |
| `build_store(corpus_dir, chunker)` | load, chunk, index — one call |
| `compare_chunkers(corpus_dir, golden, chunkers, k=3)` | `{name: hit_rate}` for a dict of named chunkers |

`compare_chunkers` is the point of the day. `build_store` taking the chunker as an
argument is what makes it possible — the same reason `chunk_documents` did on Monday.

---

## Debugging, round nine

| File | Should print |
|---|---|
| `broken_1.py` | `Hit rate: 0.5` |
| `broken_2.py` | `Chunks: 6` |
| `broken_3.py` | `Top source: expenses.md` |

- **`broken_1.py`** measures case-sensitively, so it scores itself too harshly.
- **`broken_2.py`** loses chunks. The index is rebuilt in the wrong place.
- **`broken_3.py`** searches before indexing everything. The answer is there and cannot
  be found.

Fill in `NOTES.md`.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 9 day 4" && git push
```

---

## Predict-then-run

Run `compare_chunkers` with four strategies, then run it again with `k=1` and `k=5`.

Which matters more on this corpus — the chunking, or `k`? Now say what you would do with
that information if you had a budget for exactly one improvement. That question, and
having a number to answer it with, is what "data-driven" actually means.

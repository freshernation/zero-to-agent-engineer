# Day 2 — Vectors and a store

> **By the end of today** you can turn text into a vector, say how alike two vectors
> are, and search a collection of them.

---

## Read / watch first

- [ ] `[INSTRUCTOR: source on embeddings and vector similarity — 25 min]`

---

## What you need to know

### A vector is a list of numbers standing in for a piece of text

That is the entire idea. `retrieval_kit.py` gives you the machinery:

```python
from retrieval_kit import inverse_document_frequencies, embed, cosine_similarity

idf = inverse_document_frequencies([chunk["text"] for chunk in chunks])
vector = embed("expense claims are due on the fifth", idf)
# {"expense": 0.31, "claims": 0.28, "due": 0.19, ...}
```

Ours is a dict of word to weight, because that is easy to look inside. A real embedding
model gives you a fixed-length list of a thousand-odd floats that mean nothing
individually. **Everything else on this page works identically either way.**

### Why the weights are not just counts

A word appearing in every document tells you nothing. "the" is in all six of ours.
A word appearing in one document tells you a lot — "escalation" only appears in the
on-call notes.

That is what `inverse_document_frequencies` measures: how rare a word is across the
whole collection. Multiply by how often it appears in this chunk, and you get a weight
that is high for *distinctive* words. TF-IDF is nothing more than that sentence.

**The idf depends on the whole collection**, which has a consequence people trip over:
add documents and every existing vector's weights change. Rebuild the index when the
collection changes.

### Cosine similarity

```python
cosine_similarity(query_vector, chunk_vector)     # 0.0 to 1.0
```

It compares **direction, not size**. Two chunks about expenses point the same way
whether one is a sentence or a page, which is exactly what you want — otherwise every
search would just return the longest chunk.

Zero means no shared words at all. In a neural embedding, zero effectively never
happens, and the useful scores live in a much narrower band. Do not build anything that
depends on a specific threshold value; compare scores to each other instead.

### A vector store is a list

```python
class VectorStore:
    def __init__(self):
        self.chunks = []
        self.vectors = []
        self.idf = {}
```

Search is: embed the query, score everything, sort, take the top few. That is a linear
scan, and for six documents it is instant.

Real vector databases exist because a linear scan over ten million chunks is not
instant. They use an approximate index — deliberately trading a little accuracy for a
lot of speed. **The interface is the same as yours: add things, search things.** When
you meet Chroma or pgvector, this is what they are doing, faster and less exactly.

### Top-k

```python
results = sorted(scored, key=lambda r: r["score"], reverse=True)[:k]
```

How many is `k`? Too few and the answer is not there. Too many and the real answer is
buried among near-misses — that is **context stuffing**, and it makes answers worse
while looking like it should make them better.

Three to five is a sensible starting point. Like chunk size, the honest answer is
whichever measures better, which is Thursday.

---

## Exercises

```bash
pytest week-09/day-2 -v
```

### 1. `store.py`

**`VectorStore()`**

| Member | Does |
|---|---|
| `add(chunks)` | store the chunks and **rebuild** the index |
| `search(query, k=3)` | `[{"score", "chunk"}, ...]`, best first |
| `search_in(query, source, k=3)` | the same, restricted to one document |
| `sources()` | the documents present, sorted |
| `__len__` | how many chunks |

`add` called twice must leave the store holding both sets **and** an idf computed over
all of it. There is a test — it is the thing people get wrong.

Searching an empty store returns `[]` rather than raising.

### 2. `analysis.py`

| Function | Returns |
|---|---|
| `best_source(results)` | the source of the top result, or `None` |
| `source_counts(results)` | `{"expenses.md": 2, "oncall.md": 1}` |
| `score_gap(results)` | the top score minus the second, rounded to 3dp — `0.0` if there is no second |
| `looks_uncertain(results, gap=0.02)` | `True` when the top two are within `gap` |
| `format_results(results)` | one line each: `"0.184  expenses.md#2  Claims are submitted..."` — the text cut to 60 characters |

`score_gap` and `looks_uncertain` matter more than they look. A confident retrieval has
a clear winner; a near-tie usually means the question was ambiguous or the answer is not
in the corpus, and knowing that lets you say "I don't know" instead of guessing.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 9 day 2" && git push
```

---

## Predict-then-run

Search for `"expenses"` and then for `"the"`.

Look at the scores. Then look at the idf weight for each word. Why does one produce a
clear winner and the other produce noise? You will have explained TF-IDF to yourself
better than any definition would.

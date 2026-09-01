# Day 1 — Chunking

> **By the end of today** you can split documents sensibly, and explain why the
> boundaries decide how well the whole system works.

---

## Read / watch first

- [ ] [**Chunking strategies for RAG**](../../content/week-09/day-1/chunking-strategies.md) — 25 min · docs: [`re` — Regular expressions](https://docs.python.org/3.14/library/re.html)

---

## What you need to know

### Why chunk at all

You cannot put a whole document library in a prompt. So you cut it into pieces, find the
pieces that look relevant, and put only those in.

Which means **the chunk is the unit of retrieval**. You never retrieve "the bit that
answers the question" — you retrieve a chunk, and either the answer is inside it or it
is not. Every decision about chunk boundaries is a decision about what can be found.

### Fixed-size chunking

```python
def fixed_chunks(text, size=400):
    return [text[i:i + size] for i in range(0, len(text), size)]
```

Simple, predictable, and it cuts sentences in half. A chunk ending
*"...claims must be in by the"* and the next starting *"fifth of the following month"*
means the answer to *"when are claims due"* is in **neither** chunk, and no amount of
clever searching will find it.

### Overlap

```python
def fixed_chunks_with_overlap(text, size=400, overlap=80):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks
```

Each chunk repeats the last bit of the one before, so a sentence cut in half appears
whole somewhere. It costs storage and it duplicates text in results, and it is usually
worth it.

**Watch the arithmetic**: `start += size - overlap`. If `overlap >= size`, `start` never
advances and you have an infinite loop — which is a real bug people ship.

### Splitting on sentences

Better still, cut where the text already cuts:

```python
import re

def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
```

`(?<=[.!?])` is a lookbehind — split *after* a full stop, keeping it. Then group
sentences up to a size limit, carrying the last one or two into the next group as
overlap.

This is better because sentences are where meaning already ends. It is not perfect —
"Dr. Smith" will fool it — and for this week it is fine. Knowing the limitation is
worth more than avoiding it.

### There is no correct chunk size

| Smaller chunks | Larger chunks |
|---|---|
| more precise — less irrelevant text | more context — the answer arrives with its surroundings |
| answers get split across boundaries | more competing text confuses the match |
| more chunks to search | fewer, cheaper |

Somewhere between 200 and 800 characters is a reasonable place to start. **The right
answer is whichever one measures better on your documents**, which is Thursday — and
"we measured it" is a much better interview answer than any number.

---

## Exercises

```bash
pytest week-09/day-1 -v
```

### 1. `chunking.py`

| Function | Returns |
|---|---|
| `fixed_chunks(text, size=400)` | consecutive slices |
| `fixed_chunks_with_overlap(text, size=400, overlap=80)` | slices that repeat the previous tail; raises `ValueError("Overlap must be smaller than size")` when it cannot advance |
| `split_sentences(text)` | the sentences, stripped, no empties |
| `sentence_chunks(text, max_chars=400, overlap_sentences=1)` | sentences grouped to a size, carrying the last one or two forward |
| `chunk_stats(chunks)` | `{"count", "mean_length", "shortest", "longest"}`, lengths rounded to whole numbers |

`sentence_chunks` must never cut a sentence in half. There is a test.

### 2. `loading.py`

| Function | Returns |
|---|---|
| `load_documents(directory)` | `[{"source": "expenses.md", "text": ...}, ...]`, sorted by source |
| `chunk_documents(documents, chunker)` | `[{"source", "text", "index"}, ...]` — `index` counts within its own document |
| `sources_of(chunks)` | the distinct sources, sorted |
| `chunks_from(chunks, source)` | just that document's chunks, in order |

`chunker` is a function taking text and returning a list — so you can pass any of
today's strategies and compare them on Thursday. That is the whole reason it is an
argument rather than hard-coded.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 9 day 1" && git push
```

---

## Predict-then-run

Chunk `corpus/expenses.md` at 200 characters with no overlap and print every chunk.

Find the one containing "must be in by the". Now answer *"when are expense claims due?"*
using **only** that chunk. You cannot — and no retrieval system built on those chunks
could either. That is the whole argument for overlap, in about ninety seconds.

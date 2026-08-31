# Week 9 — Retrieval, and proving it works

> **Destination**
> Build RAG over a real set of documents, and produce a **number** that says whether
> the retrieval is any good.

Building RAG takes an afternoon. Knowing whether it works is the whole week — and it is
the thing that separates a demo from something people rely on.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Split documents into chunks, and see why the boundaries matter |
| Tue | `day-2/` | Turn text into vectors, compare them, and build a store |
| Wed | `day-3/` | Retrieve, put it in a prompt, and answer with citations |
| Thu | `day-4/` | **Measure it.** Golden sets, hit rate, and a change you can prove |
| Fri | `milestone/` | RAG over the corpus, plus a measured before-and-after |

---

## The question almost nobody can answer

> *"How did you know your retrieval was any good?"*

Most junior candidates have nothing. They say it seemed to work, or that the answers
looked right. By Friday you will say:

> *"Hit rate at three was 0.65 with fixed-size chunks. I switched to sentence-aware
> chunking with one sentence of overlap and it went to 0.85. Here is the harness, and
> here are the three questions it still misses and why."*

That answer is worth more than another feature. It is also the shape of every serious
conversation about a machine learning system: not *does it work*, but *how do you know,
and what does it still get wrong*.

---

## The corpus

`week-09/corpus/` holds six documents from a fictional company — onboarding, expenses,
deployment, on-call, code review, security. Short enough to read in ten minutes, and
you should, because you cannot judge retrieval over documents you have never seen.

---

## The four ways retrieval fails

Learn these names. They come up in interviews and they are how you debug.

| Failure | What happened |
|---|---|
| **Retrieval miss** | the right passage was never fetched |
| **Wrong chunk** | something related but not the answer came back |
| **Context stuffing** | the right passage was fetched, buried among nine wrong ones |
| **Lost in the middle** | it was in the prompt, and the model looked past it |

When a RAG system answers badly, the useful first question is *which of these four was
it* — because they have completely different fixes, and three of them are not in the
prompt.

# Day 3 — Retrieval-augmented generation

> **By the end of today** you can answer a question from your documents, cite where the
> answer came from, and refuse to answer when it is not there.

Monday and Tuesday were the retrieval half. Today is the generation half, and it is
much shorter than people expect: **RAG is search results pasted into a prompt.** That is
not a simplification.

---

## Read / watch first

- [ ] [**RAG prompt construction**](../../content/week-09/day-3/rag-prompt-construction.md) — 20 min · docs: [Reduce hallucinations](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

---

## What you need to know

### The whole thing

```
question -> search the store -> put the top chunks in a prompt -> ask the model
```

Four steps. Two of them you built already, one is an f-string, and one is week 6.

### The context block

```
[expenses.md#2]
Claims are submitted monthly and must be in by the fifth of the following month.

[oncall.md#0]
The on-call rotation is one week long...
```

Label every chunk with where it came from. Two reasons, and the second is the important
one:

1. The model can cite it
2. **You** can check the citation

A RAG answer without sources is unverifiable, and unverifiable answers are how people
end up trusting a confidently wrong system. The label is the whole difference.

### The system prompt

```
Answer the question using ONLY the context provided.

Rules:
- Cite the source of every fact, like [expenses.md#2]
- If the context does not contain the answer, say exactly:
  "I don't know based on the documents I have."
- Do not use anything you know from outside the context
```

That last rule is the one that matters and the one models find hardest. A model asked
about expense policy will happily supply a *plausible general* answer about expense
policy — which is worse than no answer, because it looks the same as a real one.

### Refusing

The refusal is a feature, not a fallback. Two places to enforce it:

**In the prompt** — the exact sentence above, so the refusal is recognisable.

**In your code, before you call the model at all** — if the top result scores near zero,
there is nothing worth sending:

```python
results = store.search(question, k=3)
if not results or results[0]["score"] < min_score:
    return {"answer": "I don't know based on the documents I have.", "sources": []}
```

That second check saves a call, saves the money, and removes the chance the model
invents something from a context of noise. Do not lean on a fixed threshold with a real
embedding model, where scores sit in a much narrower band — compare to the other scores
rather than to a constant.

### Lost in the middle

Models attend most reliably to the **start and end** of a long context and least
reliably to the middle. So a chunk ranked third of nine can be present and still
overlooked.

Two practical consequences: keep `k` small, and put the best chunk **first**. Ours are
already sorted best-first, which is not an accident.

---

## Exercises

```bash
pytest week-09/day-3 -v
```

`chunking.py`, `loading.py` and `store.py` are given — this week's earlier answers.

### 1. `prompting.py`

| Thing | Does |
|---|---|
| `RAG_SYSTEM` | the system prompt: only the context, cite sources, the exact refusal sentence |
| `format_context(results)` | `[source#index]` then the text, blank line between |
| `build_rag_prompt(question, results)` | the question and the fenced context in one string |
| `citation_for(chunk)` | `"[expenses.md#2]"` |

`build_rag_prompt` must put the context inside a fence — week 6's rule, and it matters
more here because the context is text you did not write.

### 2. `rag.py`

| Function | Returns |
|---|---|
| `answer(client, store, question, k=3)` | `{"answer", "sources", "results"}` |
| `answer_or_decline(client, store, question, k=3, min_score=0.01)` | the same, but declines **without calling the model** when nothing scores |
| `cited_sources(text)` | every `[source#index]` in an answer, in order, no repeats |
| `is_refusal(text)` | `True` if the answer is the refusal sentence |

`sources` is the list of sources actually retrieved. `results` is what came back from the
store, so a caller can check the citations.

---

## Before you close the laptop

```bash
git add -A && git commit -m "week 9 day 3" && git push
```

Read the milestone tonight. Tomorrow is the week's real content.

---

## Predict-then-run

Ask your RAG system *"what is the company's parental leave policy?"* — which is in none
of the six documents.

Does it refuse? Now delete the refusal instruction from the system prompt and ask again.

What you get the second time is the single most dangerous failure mode in this
technology: an answer with the same tone, the same confidence, and no basis at all.

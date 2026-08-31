# Week 9 — Concept fence

## Allowed

**Everything from Weeks 1–8**, plus:

- `retrieval_kit.py` — `tokenise`, `term_frequencies`,
  `inverse_document_frequencies`, `embed`, `cosine_similarity` (given to you)
- `re.split` for sentence boundaries
- Your own vector store — a list of dicts is a vector store
- Golden question sets, hit rate, precision at k, recall at k
- Everything from week 8 (LangGraph, `@tool`) — the milestone builds on it

## Not yet

Chroma, FAISS, Pinecone, pgvector or any other vector database · `langchain`'s
`RecursiveCharacterTextSplitter` — **you write the splitter** · reranking models ·
GraphRAG · hybrid BM25 + vector search · fine-tuned embeddings · RAGAS and other eval
frameworks · LangSmith (week 11)

---

## About the embeddings

`retrieval_kit.py` uses **TF-IDF**, not a neural embedding model. That is a real
retrieval method, it is deterministic, and it needs no key, no model download and no
network — so every number you produce this week is reproducible on any machine.

The honest difference: **TF-IDF matches words. A neural embedding matches meaning.** A
question phrased with none of the passage's words will be found by an embedding model
and missed by TF-IDF, and you will watch exactly that happen on Thursday.

What does **not** change when you swap them:

- how you split documents into chunks
- how you choose top-k
- how you put retrieved text into a prompt
- **how you measure whether any of it worked**

That last one is the week. Everything you build here transfers unchanged, which is why
it is worth learning on something you can see all the way inside.

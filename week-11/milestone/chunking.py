"""Week 9's chunking, given to you complete."""

import re

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def fixed_chunks(text, size=400):
    """Return consecutive slices of the text."""
    return [text[i:i + size] for i in range(0, len(text), size)]


def fixed_chunks_with_overlap(text, size=400, overlap=80):
    """Return slices that each repeat the tail of the one before."""
    if overlap >= size:
        raise ValueError("Overlap must be smaller than size")

    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def split_sentences(text):
    """Return the sentences, stripped, with no empties."""
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def sentence_chunks(text, max_chars=400, overlap_sentences=1):
    """Group whole sentences up to a size, carrying the last few forward."""
    sentences = split_sentences(text)
    if not sentences:
        return []

    chunks = []
    current = []

    for sentence in sentences:
        current.append(sentence)
        if sum(len(s) for s in current) >= max_chars:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:] if overlap_sentences else []

    if current and (not chunks or " ".join(current) != chunks[-1]):
        chunks.append(" ".join(current))

    return chunks


def chunk_stats(chunks):
    """Return the shape of a set of chunks, for comparing strategies."""
    if not chunks:
        return {"count": 0, "mean_length": 0, "shortest": 0, "longest": 0}

    lengths = [len(chunk) for chunk in chunks]
    return {
        "count": len(chunks),
        "mean_length": round(sum(lengths) / len(lengths)),
        "shortest": min(lengths),
        "longest": max(lengths),
    }

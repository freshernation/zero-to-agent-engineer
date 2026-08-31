"""The scoring half of retrieval, given to you.

Real systems turn text into vectors with a neural embedding model. This uses
TF-IDF instead - a genuine, widely used retrieval method that needs no model, no
key and no network, and gives the same answer every run.

What that changes: TF-IDF matches WORDS. A neural embedding matches MEANING, so
it would find "how do I claim for a train ticket" against a passage about travel
expenses even with no shared words. Swapping one for the other is a few lines.

What it does NOT change - and this is the week's point - is anything about
chunking, about top-k, or about how you measure whether retrieval worked. Every
technique this week transfers unchanged to a real embedding model, which is why
it is worth learning on something you can see inside.
"""

import math
import re
from collections import Counter

WORD = re.compile(r"[a-z0-9]+")


def tokenise(text):
    """Return the lowercase words in a piece of text."""
    return WORD.findall(text.lower())


def term_frequencies(text):
    """Return how often each word appears, as a fraction of the whole."""
    words = tokenise(text)
    if not words:
        return {}
    counts = Counter(words)
    total = len(words)
    return {word: count / total for word, count in counts.items()}


def inverse_document_frequencies(documents):
    """Return how rare each word is across the whole collection.

    A word in every document tells you nothing; a word in one document tells you
    a lot. That is the whole idea.
    """
    total = len(documents)
    appearances = Counter()
    for document in documents:
        for word in set(tokenise(document)):
            appearances[word] += 1
    return {
        word: math.log((total + 1) / (count + 1)) + 1
        for word, count in appearances.items()
    }


def embed(text, idf):
    """Turn a piece of text into a vector, as a dict of word to weight."""
    return {
        word: frequency * idf.get(word, 1.0)
        for word, frequency in term_frequencies(text).items()
    }


def cosine_similarity(a, b):
    """Return how alike two vectors are, from 0.0 to 1.0."""
    shared = set(a) & set(b)
    if not shared:
        return 0.0
    dot = sum(a[word] * b[word] for word in shared)
    size_a = math.sqrt(sum(value * value for value in a.values()))
    size_b = math.sqrt(sum(value * value for value in b.values()))
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (size_a * size_b)

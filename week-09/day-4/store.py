"""Tuesday's store, given to you complete.
"""

from retrieval_kit import cosine_similarity, embed, inverse_document_frequencies


class VectorStore:
    def __init__(self):
        self.chunks = []
        self.vectors = []
        self.idf = {}

    def __len__(self):
        return len(self.chunks)

    def add(self, chunks):
        """Add chunks and rebuild the index over everything held."""
        self.chunks.extend(chunks)
        self._rebuild()

    def _rebuild(self):
        """idf depends on the whole collection, so it cannot be computed once."""
        texts = [chunk["text"] for chunk in self.chunks]
        self.idf = inverse_document_frequencies(texts)
        self.vectors = [embed(text, self.idf) for text in texts]

    def _scored(self, query, candidates):
        query_vector = embed(query, self.idf)
        return sorted(
            (
                {
                    "score": cosine_similarity(query_vector, self.vectors[position]),
                    "chunk": self.chunks[position],
                }
                for position in candidates
            ),
            key=lambda result: result["score"],
            reverse=True,
        )

    def search(self, query, k=3):
        """Return the k closest chunks, best first."""
        if not self.chunks:
            return []
        return self._scored(query, range(len(self.chunks)))[:k]

    def search_in(self, query, source, k=3):
        """Return the k closest chunks from one document only."""
        positions = [
            position
            for position, chunk in enumerate(self.chunks)
            if chunk["source"] == source
        ]
        if not positions:
            return []
        return self._scored(query, positions)[:k]

    def sources(self):
        """Return the documents present, sorted."""
        return sorted({chunk["source"] for chunk in self.chunks})

# Should print:  Chunks: 6
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from retrieval_kit import embed, inverse_document_frequencies


class Store:
    def __init__(self):
        self.chunks = []
        self.vectors = []
        self.idf = {}

    def add(self, chunks):
        texts = [c["text"] for c in chunks]
        self.idf = inverse_document_frequencies(texts)
        self.vectors = [embed(t, self.idf) for t in texts]
        self.chunks.extend(chunks)

    def __len__(self):
        return len(self.vectors)


store = Store()
store.add([{"text": f"chunk {n}", "source": "a.md", "index": n} for n in range(3)])
store.add([{"text": f"chunk {n}", "source": "b.md", "index": n} for n in range(3)])

print("Chunks:", len(store))

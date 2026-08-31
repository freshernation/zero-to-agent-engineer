# Should print:  Top source: expenses.md
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from chunking import sentence_chunks
from loading import chunk_documents, load_documents
from store import VectorStore

CORPUS = Path(__file__).parent.parent / "corpus"

documents = load_documents(str(CORPUS))
chunks = chunk_documents(documents, lambda t: sentence_chunks(t, 400, 1))

store = VectorStore()
store.add(chunks[:4])

results = store.search("when must expense claims be submitted", k=1)
print("Top source:", results[0]["chunk"]["source"] if results else "none")

"""Week 9's loading, given to you complete."""

from pathlib import Path


def load_documents(directory):
    """Return every document in a directory, sorted by filename."""
    documents = []
    for path in sorted(Path(directory).glob("*.md")):
        documents.append({"source": path.name, "text": path.read_text()})
    return documents


def chunk_documents(documents, chunker):
    """Chunk every document, remembering where each chunk came from."""
    chunks = []
    for document in documents:
        for index, text in enumerate(chunker(document["text"])):
            chunks.append(
                {"source": document["source"], "text": text, "index": index}
            )
    return chunks


def sources_of(chunks):
    """Return the distinct documents these chunks came from."""
    return sorted({chunk["source"] for chunk in chunks})


def chunks_from(chunks, source):
    """Return one document's chunks, in order."""
    return [chunk for chunk in chunks if chunk["source"] == source]

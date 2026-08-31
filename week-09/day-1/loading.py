# load_documents(directory)            [{"source": "expenses.md", "text": ...}, ...]
#                                      sorted by source
# chunk_documents(documents, chunker)  [{"source", "text", "index"}, ...]
#                                      index counts within its own document
# sources_of(chunks)                   the distinct sources, sorted
# chunks_from(chunks, source)          that document's chunks, in order
#
# chunker is a FUNCTION taking text and returning a list, so you can pass any
# strategy in and compare them on Thursday.

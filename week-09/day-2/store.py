# VectorStore()
#   add(chunks)                store the chunks and REBUILD the index
#   search(query, k=3)         [{"score", "chunk"}, ...], best first
#   search_in(query, source, k=3)   the same, restricted to one document
#   sources()                  the documents present, sorted
#   __len__                    how many chunks
#
# add() twice must leave BOTH sets stored and the idf computed over all of it.
# Searching an empty store returns [] rather than raising.
#
# from retrieval_kit import inverse_document_frequencies, embed, cosine_similarity

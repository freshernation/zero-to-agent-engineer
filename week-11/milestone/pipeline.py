# Assistant(corpus_dir, chunker=None, k=3, min_score=0.01)
#
#   build()        load, chunk, index - returns self
#   chunk_count    how many chunks
#   sources        the document names, sorted
#   answer(client, question, request_id, clock)
#       {"answer", "sources", "refused", "request_id", "trace", "duration_ms"}
#
# Open a span for "retrieve" and one for "generate".
# Refuse WITHOUT calling the model when nothing scores. Cite sources.

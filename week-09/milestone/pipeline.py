# RagSystem(chunker, k=3, min_score=0.01)     No printing.
#
#   build(corpus_dir)          load, chunk, index - returns self
#   search(question)           the top k results
#   answer(client, question)   {"answer", "sources", "results", "refused"}
#   chunk_count                how many chunks are indexed
#
# answer() declines WITHOUT calling the model when the top score is below
# min_score, sets refused=True, and uses exactly:
#   I don't know based on the documents I have.

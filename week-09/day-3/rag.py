# answer(client, store, question, k=3)
#     {"answer", "sources", "results"}
#
# answer_or_decline(client, store, question, k=3, min_score=0.01)
#     the same, but declines WITHOUT calling the model when nothing scores
#
# cited_sources(text)   every [source#index] in an answer, in order, no repeats
# is_refusal(text)      True if the answer is the refusal sentence

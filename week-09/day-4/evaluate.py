# is_hit(results, expected)          True if any retrieved chunk contains the
#                                    phrase, ignoring case
# hit_rate(store, golden, k=3)       the fraction, rounded to 3dp
# misses(store, golden, k=3)         the questions that failed, in order
# evaluate(store, golden, k=3)       {"hit_rate", "hits", "total", "misses"}
# build_store(corpus_dir, chunker)   load, chunk, index - one call
# compare_chunkers(corpus_dir, golden, chunkers, k=3)
#                                    {name: hit_rate} for a dict of named chunkers

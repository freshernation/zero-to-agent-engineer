# fixed_chunks(text, size=400)
# fixed_chunks_with_overlap(text, size=400, overlap=80)
#     raises ValueError("Overlap must be smaller than size") when it cannot advance
# split_sentences(text)        stripped, no empties
# sentence_chunks(text, max_chars=400, overlap_sentences=1)
#     never cuts a sentence in half
# chunk_stats(chunks)          {"count", "mean_length", "shortest", "longest"}
#                              lengths rounded to whole numbers
#
# import re
# re.split(r"(?<=[.!?])\s+", text) splits AFTER a full stop, keeping it

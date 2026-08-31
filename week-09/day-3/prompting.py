# RAG_SYSTEM                      the system prompt: use ONLY the context,
#                                 cite every fact like [expenses.md#2], and if
#                                 the answer is not there say exactly:
#                                   I don't know based on the documents I have.
#
# format_context(results)         "[source#index]\n<text>" per result,
#                                 blank line between
# build_rag_prompt(question, results)   the question plus the FENCED context
# citation_for(chunk)             "[expenses.md#2]"

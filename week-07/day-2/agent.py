# Import from toolkit.py - do not rewrite it.
#
#   tool_result_message(pairs)
#       a user message dict with one tool_result block per (id, result) pair
#
#   run(client, question, max_iterations=5)              the final text
#   iterations_used(client, question, max_iterations=5)  how many model calls
#   run_with_trace(client, question, max_iterations=5)   (final_text, trace)
#
# On hitting the cap, run() returns exactly:
#   Stopped after 5 steps without finishing.
#
# Trace entries:
#   {"step": 1, "type": "tool_call", "name": ..., "input": ..., "result": ...}
#   {"step": 2, "type": "answer", "text": ...}
#
# Write the iteration cap FIRST.

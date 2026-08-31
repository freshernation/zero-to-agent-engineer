# Agent(client, max_iterations=6, max_repeats=2)
#
#   run(question)   the final answer
#   trace           the record of the run
#   stop_reason     "answered" | "cap" | "looping"
#   model_calls     how many model calls
#   last_answer     the most recent answer
#
# Unknown tool  -> "Unknown tool: <name>", loop carries on
# Tool raises   -> "Tool failed: <message>", loop carries on
# Long results  -> truncated at 500 characters
# Repeated call -> "Stopped: the agent repeated the same tool call."
# Cap reached   -> "Stopped after N steps without finishing."
#
# Write the cap first.

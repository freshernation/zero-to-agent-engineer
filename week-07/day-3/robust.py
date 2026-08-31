# Agent(client, max_iterations=5, max_repeats=2)
#
#   run(question)   the final answer
#   trace           same shape as day 2
#   stop_reason     "answered" | "cap" | "looping"
#   model_calls     how many times the model was called
#
# Unknown tool  -> result "Unknown tool: <name>", loop carries on
# Tool raises   -> result "Tool failed: <message>", loop carries on
# Long results  -> truncated at 500 characters
# Repeated call -> "Stopped: the agent repeated the same tool call."
# Cap reached   -> "Stopped after N steps without finishing."

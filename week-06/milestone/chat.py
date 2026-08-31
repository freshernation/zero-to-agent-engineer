# Conversation(system=None, max_turns=10)   No printing. No input.
#
#   messages                       history, trimmed, always starting with user
#   add_user(text) / add_assistant(text)
#   send(client, text)             ask, record both sides, return the reply
#   stream(client, text, write)    the same, calling write(chunk) as text arrives
#   total_cost(input_rate, output_rate)      to 6dp
#   turn_count
#   reset()                        forget everything, including the cost
#
# stream() must record the reply in the history too.

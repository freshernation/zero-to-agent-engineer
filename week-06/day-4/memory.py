# trim(messages, max_turns)                 last max_turns, still starting with user
# estimate_conversation_tokens(messages)    one token per 4 chars of content,
#                                           rounded UP per message
# needs_trimming(messages, budget)          True if the estimate exceeds the budget
#
# class Conversation(system=None, max_turns=10)
#     add_user(text) / add_assistant(text)
#     messages                              current list, trimmed
#     send(client, text)                    ask, record the reply, return it
#     total_cost(input_per_million, output_per_million)     to 6dp
#     __len__
#
# trim must never leave the history starting with an assistant turn.

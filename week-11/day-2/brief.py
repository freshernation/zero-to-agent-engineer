# build_brief(goal, known, return_format)
#     the text handed to a worker, in three labelled parts:
#
#         Goal: Find the population of Lisbon.
#
#         What is known:
#         - The user wants a total for two cities
#         - Lagos is already done: 15400000
#
#         Return: The number, digits only.
#
#     known is a list of strings. An empty list gives one line:  - nothing yet
#     ValueError when goal or return_format is empty or only spaces.
#
# missing_parts(brief)
#     which of "Goal", "What is known", "Return" do not start a line of the
#     brief, followed by a colon. In that order. Any capitals.
#
# estimate_tokens(text)          len(text) // 4
# crossed(brief, report)         tokens that crossed the handoff, both ways
# kept_out(result, report)       tokens the worker used that the asker never
#                                saw: its input + output tokens, minus the
#                                report. Never below zero.
# lost(result, report)           the tool results in result["tool_calls"] whose
#                                text does not appear in the report, in order

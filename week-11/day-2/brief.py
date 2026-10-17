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
#
# A budget per worker. Every report lands in the ORCHESTRATOR's context, which
# all the workers share. One worker that sends back a page leaves less room for
# everyone else - so each gets a share, and is held to it.
#
# report_budget(window, reserve, workers)
#     the tokens each worker's report may use: (window - reserve) // workers,
#     where reserve is what the orchestrator keeps for its own instructions,
#     the task and its answer. ValueError for no workers, or a reserve that
#     leaves nothing.
#
# fit_report(report, budget)
#     the report unchanged if estimate_tokens(report) <= budget. Otherwise its
#     first budget * 4 characters, then
#         " [cut: 1600 characters over this worker's budget]"
#     A cut report says so. A silently short one is a lost fact.
#
# over_budget(results, budget)
#     the "worker" names, in order, whose own input_tokens went above budget:
#     the workers whose OWN window filled up, even if their reports were short


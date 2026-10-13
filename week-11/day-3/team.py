# from agent_kit import run_agent
# from worker import worker_schema, run_worker, report      (given)
#
# ORCHESTRATOR_SYSTEM
#     the orchestrator's instructions. It cannot look anything up or work
#     anything out itself - it can only ask a worker, with a brief.
#
# run_team(client, question, workers, max_delegations=4, max_steps=8)
#     runs an orchestrator whose ONLY tools are the workers, and returns:
#
#       "text"          the orchestrator's final answer
#       "stopped"       "answered" or "cap"
#       "delegations"   [{"worker": name, "brief": ..., "report": ...}, ...]
#       "model_calls"   {"orchestrator": n, "<worker name>": n, ...}
#                       every worker is listed, 0 if it was never asked
#       "total_calls"   all of them added up
#
# The orchestrator is run_agent. Its tools are functions that take a brief,
# run a worker, and hand back report(result).
#
# Three things a delegation must never do:
#   - crash the team. A worker that RAISES gives the report
#         "Worker <name> failed: <the error>"
#   - go on for ever. Past max_delegations the worker is NOT run and the
#     report is
#         "Refused: delegation limit of <n> reached."
#   - go missing. Every delegation, refused or not, is in "delegations".

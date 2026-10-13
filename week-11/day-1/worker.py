# from agent_kit import run_agent      (given - read it first)
#
# make_worker(name, description, system, schemas, tools, client)
#     a dict with exactly those six keys
#
# worker_schema(worker)
#     the tool schema an orchestrator is offered for this worker:
#       name          "ask_<worker name>"
#       description   the worker's description, unchanged
#       input_schema  one required string argument called "brief", with a
#                     description of its own
#
# run_worker(worker, brief, max_steps=6)
#     runs the worker's own agent on the brief, from an EMPTY conversation,
#     with the worker's own client, system prompt, schemas and tools.
#     Returns run_agent's result with one more key:  "worker": <name>
#
# report(result)
#     the string that goes back to whoever asked:
#       the worker's text, when it answered
#       "Worker <name> did not finish: <text>"  when it stopped any other way

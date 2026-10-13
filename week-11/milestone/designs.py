# from agent_kit import run_agent, SCHEMAS, TOOLS, LOOKUP_SCHEMA, CALCULATE_SCHEMA,
#                       lookup_population, calculate
# from worker import make_worker           (given)
# from team import run_team                (given)
#
# run_single(client, question)
#     ONE agent holding both tools. Returns run_agent's result.
#
# build_team(researcher_client, analyst_client)
#     [researcher, analyst] - two workers, in that order.
#       researcher   holds lookup_population and nothing else
#       analyst      holds calculate and nothing else
#     Each needs a description an orchestrator can choose from, and a system
#     prompt of its own.
#
# run_as_team(orchestrator_client, question, workers)
#     run_team's result

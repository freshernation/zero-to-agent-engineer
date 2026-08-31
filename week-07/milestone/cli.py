# The program a person runs.
#
#   > <anything>   runs the agent, prints the answer
#   /trace         the last run's trace, one line per step
#                  ("No runs yet." before any question)
#   /stop          "Stop reason: answered"
#   /quit          "Bye." and stops
#
# --real uses the real client if ANTHROPIC_API_KEY is set.

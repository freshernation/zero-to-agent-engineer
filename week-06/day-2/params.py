# All four return the reply text. The tests check what you SENT.
#
#   quick(client, prompt)                  output_config={"effort": "low"}
#   thorough(client, prompt)               output_config={"effort": "high"}
#   one_line(client, prompt)               stop_sequences=["\n"]
#   with_system(client, system, prompt)    the system prompt in the system field

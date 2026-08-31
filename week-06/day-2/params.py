# All four return the reply text. The tests check what you SENT.
#
#   precise(client, prompt)                temperature=0
#   creative(client, prompt)               temperature=1.0
#   one_line(client, prompt)               stop_sequences=["\n"]
#   with_system(client, system, prompt)    the system prompt in the system field

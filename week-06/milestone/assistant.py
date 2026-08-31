# The program. All printing and asking lives here.
#
#   > <anything>     streams the model's reply
#   /note <text>     extracts a Note and prints it, or "Could not extract a note."
#   /cost            "Spent so far: $0.001035"
#   /turns           "Turns: 4"
#   /reset           clears history, prints "Forgotten."
#   /quit            prints "Total: $0.001035" and stops
#   /banana          "Unknown command: /banana"
#
# A failed model call prints:
#   The model is unavailable right now. Try again.
# and the loop carries on. Never a traceback.
#
# See README.md for the Note print format.

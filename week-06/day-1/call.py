# Every function takes client first. The tests pass in a FakeClient.
#
#   ask(client, question, model="claude-sonnet-4-5", max_tokens=1000)
#       the reply text
#
#   extract_text(response)
#       every text block joined, ignoring any other kind of block
#
#   was_truncated(response)
#       True if stop_reason is "max_tokens"
#
#   ask_safely(client, question, max_tokens=1000)
#       the reply, or None if it was truncated

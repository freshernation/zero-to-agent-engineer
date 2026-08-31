# call_signature(name, arguments)      a stable string; argument ORDER must not matter
# count_calls(signatures, name, arguments)     how many times that call already appears
# is_repeating(signatures, name, arguments, limit=2)
#                                      True when it has already happened `limit` times
# validate_arguments(schema, arguments)
#                                      (True, "") or
#                                      (False, "missing required argument: expression")
#                                      (False, "unexpected argument: expr")
# truncate(text, max_chars=500)        the text, or max_chars plus "... [truncated]"
#
# Missing required arguments are reported before unexpected ones.

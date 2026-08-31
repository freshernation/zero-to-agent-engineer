# new_request_id()          12 lowercase hex characters
# redact(fields, secret_keys=("api_key", "authorization", "token"))
#                           those values replaced by "****", case-insensitive,
#                           including nested dicts
# log_line(level, event, **fields)   a JSON string with level, event and the
#                                    fields, redacted
# parse(line)               the JSON back to a dict

# Tracer(request_id, clock)
#   span(name, **metadata)   a context manager; nests inside whatever is open
#   to_dict()                {"request_id", "spans": [...]} - a tree with
#                            name, duration_ms, metadata, children
#   total_ms()               the whole request
#   flatten()                [(depth, name, duration_ms), ...] in start order
#   slowest()                name of the slowest TOP-LEVEL span
#
# A span object has .set(key, value).
# clock returns float seconds; durations are whole milliseconds.
#
# A span whose body RAISES must still be closed and recorded, with
# metadata["error"] set to the exception's message.

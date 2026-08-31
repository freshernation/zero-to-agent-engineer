# format_step(entry)    one readable line for a trace entry
#     tool call:  1. calculate({'expression': '17 * 23'}) -> 391
#     answer:     2. answer: 17 * 23 is 391.
#
# format_trace(trace)   the whole trace, one line per entry
# tool_names(trace)     every tool name called, in order, repeats included
# summarise(trace)      "3 steps, 2 tool calls (calculate, city_info)"

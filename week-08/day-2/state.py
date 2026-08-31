# CounterState(TypedDict)   count: int, limit: int,
#                           log: a list that ACCUMULATES
#
#   increment(state)          count + 1, "incremented" on the log
#   double(state)             count * 2, "doubled" on the log
#   is_even(state)            True if count is even
#   route_by_parity(state)    "double" when even, END when not
#   route_until_limit(state)  "increment" while count < limit, END otherwise
#
# from typing import Annotated, TypedDict
# from langgraph.graph import END
# import operator

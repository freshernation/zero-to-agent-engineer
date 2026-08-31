# build_linear()      START -> increment -> double -> END
# build_branching()   START -> increment -> (even?) -> double -> END, else END
# build_loop()        START -> increment -> (under limit?) -> increment, else END
#
# Each returns a COMPILED graph.
# initial(count=0, limit=5)   a starting state dict
#
# from langgraph.graph import StateGraph, START, END

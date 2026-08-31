# Should print:  Alice: 3 steps  Bob: 2 steps
#
# Alice needs three increments and Bob needs two. Count the log entries.
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    count: int
    limit: int
    log: Annotated[list, operator.add]


def increment(state):
    return {"count": state["count"] + 1, "log": ["incremented"]}


def route(state):
    return "increment" if state["count"] < state["limit"] else END


graph = StateGraph(State)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_conditional_edges("increment", route, ["increment", END])
app = graph.compile(checkpointer=MemorySaver())

CONFIG = {"configurable": {"thread_id": "shared"}}

alice = app.invoke({"count": 0, "limit": 3, "log": []}, CONFIG)
bob = app.invoke({"count": 0, "limit": 2, "log": []}, CONFIG)

print("Alice:", len(alice["log"]), "steps  Bob:", len(bob["log"]), "steps")

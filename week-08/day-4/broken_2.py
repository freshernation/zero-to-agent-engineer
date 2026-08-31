# Should print:  Visits: 3
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    count: int
    limit: int
    log: Annotated[list, operator.add]


def visit(state):
    return {"count": state["count"] + 1, "log": ["visited"]}


def route(state):
    return "visit" if state["count"] <= state["limit"] else END


graph = StateGraph(State)
graph.add_node("visit", visit)
graph.add_edge(START, "visit")
graph.add_conditional_edges("visit", route, ["visit", END])

result = graph.compile().invoke({"count": 0, "limit": 3, "log": []})
print("Visits:", len(result["log"]))

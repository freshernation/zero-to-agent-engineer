# Should print:  Log: ['added', 'doubled']
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    value: int
    log: Annotated[list, operator.add]


def double(state):
    return {"value": state["value"] * 2, "log": ["doubled"]}


def add_one(state):
    return {"value": state["value"] + 1, "log": ["added"]}


child_graph = StateGraph(State)
child_graph.add_node("double", double)
child_graph.add_edge(START, "double")
child_graph.add_edge("double", END)
child = child_graph.compile()

parent = StateGraph(State)
parent.add_node("add_one", add_one)
parent.add_node("child", child)
parent.add_edge(START, "add_one")
parent.add_edge("add_one", "child")
parent.add_edge("child", END)

print("Log:", parent.compile().invoke({"value": 3, "log": []})["log"])

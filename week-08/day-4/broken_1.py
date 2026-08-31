# Should print:  Log: ['a', 'b']
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    log: list


def first(state):
    return {"log": ["a"]}


def second(state):
    return {"log": ["b"]}


graph = StateGraph(State)
graph.add_node("first", first)
graph.add_node("second", second)
graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)

print("Log:", graph.compile().invoke({"log": []})["log"])

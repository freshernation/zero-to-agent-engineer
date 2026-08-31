# Should print:  Log: ['prepared', 'spent']
#
# The invoke looks fine. The complaint arrives when you ask where it got to.
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    amount: int
    log: Annotated[list, operator.add]


def prepare(state):
    return {"log": ["prepared"]}


def spend(state):
    return {"log": ["spent"]}


graph = StateGraph(State)
graph.add_node("prepare", prepare)
graph.add_node("spend", spend)
graph.add_edge(START, "prepare")
graph.add_edge("prepare", "spend")
graph.add_edge("spend", END)

app = graph.compile(interrupt_before=["spend"])

config = {"configurable": {"thread_id": "t1"}}
app.invoke({"amount": 500, "log": []}, config)

print("Log:", app.get_state(config).values.get("log"))

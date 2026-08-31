# Should print:  Answer: It is 391.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Annotated, TypedDict

from fake_chat import FakeChat, ai, ai_tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from toolkit import all_tools, tool_by_name


class State(TypedDict):
    messages: Annotated[list, add_messages]
    steps: int


model = FakeChat([
    ai_tool("calculate", {"expression": "17 * 23"}, id="t1"),
    ai("It is 391."),
])
bound = model.bind_tools(all_tools())


def call_model(state):
    return {"messages": [bound.invoke(state["messages"])], "steps": state["steps"] + 1}


def run_tools(state):
    last = state["messages"][-1]
    results = []
    for call in last.tool_calls:
        content = str(tool_by_name(call["name"]).invoke(call["args"]))
        results.append(ToolMessage(content=content, tool_call_id=call["id"]))
    return {"messages": results}


def route(state):
    if state["steps"] >= 5:
        return END
    return "tools" if getattr(state["messages"][-1], "tool_calls", None) else END


graph = StateGraph(State)
graph.add_node("model", call_model)
graph.add_node("tools", run_tools)
graph.add_edge(START, "model")
graph.add_conditional_edges("model", route, ["tools", END])
graph.add_edge("tools", END)

state = graph.compile().invoke(
    {"messages": [HumanMessage("What is 17 * 23?")], "steps": 0}
)

answer = ""
for message in reversed(state["messages"]):
    if isinstance(message, AIMessage) and message.content:
        answer = message.content
        break

print("Answer:", answer)

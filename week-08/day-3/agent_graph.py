# AgentState(TypedDict)   messages: Annotated[list, add_messages]
#                         steps: int
#
#   make_call_model(model)          returns the model node for that model
#   run_tools(state)                the tools node - one ToolMessage per call
#   make_route(max_steps)           returns the router
#   build_agent(model, max_steps=6) the compiled graph
#   run(model, question, max_steps=6)             the final text
#   run_with_state(model, question, max_steps=6)  (final_text, final_state)
#
# On hitting the cap: the last text you have, or
#   "Stopped after 6 steps without finishing."
#
# run_tools handles an unknown tool and a tool that raises - a ToolMessage
# comes back either way, and the graph carries on.
#
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langchain_core.messages import HumanMessage, ToolMessage

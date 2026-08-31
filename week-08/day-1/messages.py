# to_langchain(messages)   week-6 dicts -> LangChain message objects
# to_dicts(messages)       the reverse
# describe(messages)       "system, human, ai" - the types in order, lowercase
# last_ai_text(messages)   content of the last AIMessage, or None
#
# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
#
# Roles map: system <-> SystemMessage, user <-> HumanMessage,
#            assistant <-> AIMessage

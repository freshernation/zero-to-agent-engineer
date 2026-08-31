# build_prompt(role)              ChatPromptTemplate with a {question} variable
#                                 and the role in the system message
# simple_chain(model, role)       prompt | model | StrOutputParser()
# ask(model, role, question)      the answer as a plain string
# bound_model(model)              the model with all four tools bound
# tool_calls_for(model, question) the tool_calls list from one bound call

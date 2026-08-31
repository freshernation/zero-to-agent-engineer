# create_app(answerer)              the FastAPI app, using the answerer given
# default_answerer(question, k)     a stub answer, so the app runs alone
#
#   GET  /health    {"status": "ok", "documents": n}
#   POST /ask       answers a question
#   GET  /sources   the document names
#
# answerer(question, k) returns {"answer", "sources", "refused"}
#
# Bad input gets a 422 and you write no code for it.
#
# from fastapi import FastAPI

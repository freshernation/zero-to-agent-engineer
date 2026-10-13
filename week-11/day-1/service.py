# create_app(answerer, api_key=None)   the FastAPI app, using the answerer given
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
# With an api_key, POST /ask needs the header  Authorization: Bearer <key>
# and anything else gets a 401 without the answerer being called.
# GET /health answers either way. With no api_key there is no check.
#
# from fastapi import FastAPI

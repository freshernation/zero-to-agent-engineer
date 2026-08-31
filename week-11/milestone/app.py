# create_app(assistant, client, settings)   the FastAPI app
#
#   GET  /health   {"status", "version", "uptime_seconds"} - cheap
#   GET  /ready    {"ready", "checks", "failing"}
#   GET  /sources  the document names
#   POST /ask      answers, with a request_id
#
# POST /ask must:
#   - 413 for a question over settings["max_question_length"]
#   - 429 when the daily budget is spent
#   - put request_id in the body AND the X-Request-ID header
#   - never return a traceback

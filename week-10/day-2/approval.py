# An expense graph: prepare -> spend. spend asks for approval before it spends.
#
# State: amount: int, approved (None | True | False), log (accumulating)
#
#   build(checkpointer)             the compiled graph
#   start(app, thread_id, amount)   run until it pauses, return the state
#   pending(app, thread_id)         the node it waits on, or None if finished
#   approve(app, thread_id)         resume with True; the spend happens
#   reject(app, thread_id)          resume with False; it does not
#   is_finished(app, thread_id)     True when nothing is next
#
# prepare logs "prepared 500"
# spend   calls interrupt(), records the answer in approved, and logs
#         "spent 500" - or "rejected" when the answer was not True
#
# app.invoke(Command(resume=...), config) resumes.
# app.get_state(config).next tells you where it stopped.

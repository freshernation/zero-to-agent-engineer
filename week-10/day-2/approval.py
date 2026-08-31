# An expense graph: prepare -> spend, pausing before spend.
#
# State: amount: int, approved (None | True | False), log (accumulating)
#
#   build(checkpointer)             compiled, pausing before "spend"
#   start(app, thread_id, amount)   run until it pauses, return the state
#   pending(app, thread_id)         the node it waits on, or None if finished
#   approve(app, thread_id)         resume; the spend happens
#   reject(app, thread_id)          set approved False, resume; it does not
#   is_finished(app, thread_id)     True when nothing is next
#
# prepare logs "prepared 500"
# spend   logs "spent 500", or "rejected" when approved is False
#
# app.invoke(None, config) resumes. app.get_state(config).next tells you where.

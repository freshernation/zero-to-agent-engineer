# The week-8 counter graph, with saving.
#
#   build(checkpointer=None)      compiled: START -> increment ->
#                                 (count < limit?) -> increment, else END
#   make_saver()                  a MemorySaver
#   config_for(thread_id)         {"configurable": {"thread_id": ...}}
#   run(app, thread_id, count=0, limit=3)   the final state
#   state_of(app, thread_id)      the values, or None if never run
#   checkpoint_count(app, thread_id)        how many checkpoints
#   set_state(app, thread_id, updates)      apply an update, return new values
#
# State: count: int, limit: int, log: a list that ACCUMULATES
#
# build() with no checkpointer must still work.
#
# from langgraph.checkpoint.memory import MemorySaver

# node_updates(app, state)         [(node_name, update), ...] from streaming
# node_sequence(app, state)        just the node names, in order, repeats included
# count_visits(app, state, node)   how many times one node ran
# final_state(app, state)          the state after the last update
#
# for update in app.stream(state):
#     # update is {"node_name": {...what it returned...}}

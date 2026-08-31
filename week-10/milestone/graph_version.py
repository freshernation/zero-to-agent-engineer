# Week 8's agent, unchanged in shape. One agent, both tools, a cap.
#
#   build(model, max_steps=6)                the compiled agent graph
#   run(model, question, max_steps=6)        the final text
#   run_with_steps(model, question, max_steps=6)   (text, model_calls)
#
# Use toolkit.py. Cap message:
#   "Stopped after 6 steps without finishing."

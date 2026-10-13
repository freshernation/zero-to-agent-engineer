# passed(text, expected)
#     True when expected appears in text, ignoring commas and capitals
#
# summarise(runs)
#     runs is [{"passed": bool, "model_calls": int}, ...], one per task
#     -> {"tasks": n, "pass_rate": to 2dp, "calls_per_task": to 1dp}
#     no runs -> all three are 0
#
# compare(single, team)
#     both are summaries
#     -> {"quality_gain": team pass_rate minus single pass_rate, to 2dp
#         "cost_ratio":   team calls_per_task / single calls_per_task, to 1dp}
#     cost_ratio is 0.0 when the single agent made no calls
#
# recommend(comparison, min_gain=0.10)
#     "team" only when quality_gain is at least min_gain.
#     Otherwise "single-agent". The dearer design has to buy something.

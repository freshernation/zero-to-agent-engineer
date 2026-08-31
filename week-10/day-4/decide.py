# REASONS                       the four reasons that hold up, as strings
# assess(requirements)          {"recommend": "single"|"multi", "reasons": [...]}
# estimate_calls(agent_count, tools_used)   agent_count + tools_used
# compare_designs(designs)      {name: estimated_calls}
# cheapest(designs)             the name of the cheapest
#
# requirements flags: different_tools, different_permissions,
#                     different_models, parallel_subtasks
# Any one justifies multi. None of them means single.
# reasons lists only the flags actually set.
#
# designs is {name: {"agent_count": n, "tools_used": m}}

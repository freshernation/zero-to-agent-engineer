# DESIGNS      {"single-agent": {"agent_count": n, "tools_used": m},
#               "crew": {...}}
# estimate(design)   agent_count + tools_used
# compare()          {name: estimate}
# ratio()            crew calls / single-agent calls, to 1dp
# recommend()        "single-agent" or "crew" - the cheaper one unless you can
#                    name a reason

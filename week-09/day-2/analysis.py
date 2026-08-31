# best_source(results)              source of the top result, or None
# source_counts(results)            {"expenses.md": 2, "oncall.md": 1}
# score_gap(results)                top score minus second, 3dp; 0.0 if no second
# looks_uncertain(results, gap=0.02)  True when the top two are within gap
# format_results(results)           "0.184  expenses.md#2  Claims are submitted..."
#                                   the text cut to 60 characters

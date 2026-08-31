# evaluate(system, golden)                    {"hit_rate", "hits", "total", "misses"}
# compare(corpus_dir, golden, configurations) {name: report} for named RagSystems
# format_comparison(reports)                  a table, one line per configuration
#     "fixed-200          0.650   13/20"
#     name left in 18, rate to 3dp, then hits/total
# improvement(reports, baseline, candidate)   difference in hit rate, 3dp

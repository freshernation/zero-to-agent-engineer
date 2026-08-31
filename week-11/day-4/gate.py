# THRESHOLDS                    hit_rate 0.80, mean_score 3.5, refusal_rate 0.20
# check(report, thresholds)     {"passed": bool, "failures": [...]}
# summarise(report, thresholds) "hit_rate 0.850 >= 0.800 PASS" per metric
# exit_code(result)             0 passed, 1 not
#
# hit_rate and mean_score must be AT OR ABOVE their thresholds.
# refusal_rate must be AT OR BELOW its own.

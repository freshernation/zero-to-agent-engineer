# JUDGE_SYSTEM   the rubric: 1-5, what each end means, JSON only
# judge(client, question, answer, reference)   {"score": int, "reason": str}
# mean_score(judgements)                       to 2dp, 0.0 for none
#
# verdict(score)                               "pass" for 4 or 5, otherwise "fail"
# agreement(judge_scores, human_scores)        share with the same verdict, to 2dp;
#                                              0.0 for none; ValueError if the
#                                              lists are different lengths
# baseline(human_scores)                       the agreement a judge gets by giving
#                                              every answer the most common human
#                                              verdict
# beats_baseline(judge_scores, human_scores)   True only when agreement is ABOVE
#                                              the baseline
#
# An unparseable or out-of-range judgement scores 0 with a reason saying so.
# A judge that crashes on its own bad output is not a judge.

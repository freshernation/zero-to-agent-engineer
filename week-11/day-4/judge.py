# JUDGE_SYSTEM   the rubric: 1-5, what each end means, JSON only
# judge(client, question, answer, reference)   {"score": int, "reason": str}
# mean_score(judgements)                       to 2dp, 0.0 for none
#
# An unparseable or out-of-range judgement scores 0 with a reason saying so.
# A judge that crashes on its own bad output is not a judge.

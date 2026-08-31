# check_question(text, max_chars)   (True, "") or
#                                   (False, "Question is too long (612 > 500)")
#
# Budget(limit)
#   spend(amount)          raises BudgetExceeded past the limit, and does NOT
#                          record the spend
#   remaining / spent      properties
#   would_exceed(amount)   True if spending it would go over
#   reset()                back to zero
#
# class BudgetExceeded(Exception): pass

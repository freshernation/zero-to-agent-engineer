"""Expense(description, amount, category)

    attributes: description, amount, category
    ValueError("Description cannot be empty")   for an empty description
    ValueError("Amount must be positive")       for zero or less
    __repr__   "Expense('Coffee', 4.5, 'food')"
    __eq__     all three match; NotImplemented against anything else

Never prints. Never asks.
"""

"""Expense(description, amount, category)

    three attributes
    __repr__    "Expense('Coffee', 4.5, 'food')"   <- note the quotes; use !r

Ledger() - starts empty, holds Expense objects

    add(expense)            appends it
    total()                 every amount, rounded to 2dp
    by_category(category)   list of the expenses in that category
    biggest()               the largest Expense, or None when empty
    __len__                 how many
    __repr__                "Ledger(3 expenses, $17.75)"
"""

"""Expense logic. No printing, no input, no crashing.

An expense is a dict:  {"description": ..., "amount": ..., "category": ...}

    parse_amount(text)                      float, or raises ValueError
                                            "Amount must be a number"
                                            "Amount cannot be negative"

    add_expense(expenses, description, amount, category)
                                            a NEW list with the expense on the end
                                            (must not change the list passed in)

    total(expenses)                         sum of amounts, rounded to 2dp
    by_category(expenses)                   {category: total}, each rounded to 2dp
    format_expense(expense)                 "{description:<20}{category:<12}${amount:>8.2f}"
    load_expenses(path)                     the saved list, or [] if missing or damaged
    save_expenses(path, expenses)           writes the list as JSON

Give every function a docstring saying what it returns.
"""

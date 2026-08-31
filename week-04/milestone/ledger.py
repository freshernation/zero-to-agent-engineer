"""Ledger() - starts empty.

    add(expense)            appends; TypeError("Can only add Expense objects")
    total()                 every amount, rounded to 2dp
    by_category(category)   the expenses in that category, in the order added
    categories()            every category present, sorted, no repeats
    biggest()               the largest Expense, or None when empty
    __len__                 how many
    __repr__                "Ledger(3 expenses, $17.75)"
    save(path)              writes the ledger as JSON

load_ledger(path)           module-level function returning a Ledger;
                            an empty one if the file is missing or damaged

Never prints. Never asks.
"""

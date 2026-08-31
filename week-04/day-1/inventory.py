"""Inventory() - starts empty.

    add(name, quantity)     adds; tops up if the name is already there
    remove(name, quantity)  takes away; raises ValueError("Not enough Widget")
    quantity_of(name)       how many, 0 if never seen
    total_items()           every quantity added together
    is_empty()              True when nothing has a quantity above zero
"""

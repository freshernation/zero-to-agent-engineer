"""Functions that refuse bad input by raising ValueError.

    parse_age(text)     -> int, or raises ValueError
    parse_amount(text)  -> float, or raises ValueError

The messages are shown to a person, so they have to be exact:

    parse_age("abc")     -> ValueError("Age must be a whole number")
    parse_age("-5")      -> ValueError("Age must be between 0 and 130")
    parse_age("200")     -> ValueError("Age must be between 0 and 130")
    parse_age("30")      -> 30

    parse_amount("abc")  -> ValueError("Amount must be a number")
    parse_amount("-3")   -> ValueError("Amount cannot be negative")
    parse_amount("4.50") -> 4.5
"""

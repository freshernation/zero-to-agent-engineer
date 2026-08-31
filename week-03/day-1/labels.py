"""Display strings. Return them - do not print them.

    price_label(amount)             "$4.50"
    initials(first, last)           "A.S."
    summary_line(name, amount)      name left-aligned in 12, a space, then price_label

    summary_line("Ana", 4.5)  ->  "Ana          $4.50"

summary_line MUST call price_label rather than formatting the money itself.
There is a test for that.
"""

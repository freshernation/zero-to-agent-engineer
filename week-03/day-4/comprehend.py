"""Comprehensions.

    doubled(numbers)                    every number times two
    long_words(words, min_length=5)     only words at least min_length long
    names_only(records)                 the "name" of every record
    price_map(items)                    dict of each item's "name" -> "price"
    top_n(records, n)                   the n records with the highest "amount",
                                        highest first

The first four must be comprehensions - a test counts them.
top_n is the one where a comprehension is the wrong tool: use sorted(key=...).
"""

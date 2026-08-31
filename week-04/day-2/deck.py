"""Card(rank, suit)

    __repr__    "Card('A', 'spades')"
    __eq__      equal when rank and suit both match

Deck(cards) - takes a list of Cards

    deal(n)     returns the first n cards AND removes them;
                raises ValueError("Not enough cards") if there are too few
    add(card)   puts one on the bottom
    __len__     how many are left
    __repr__    "Deck(52 cards)"

Get the order right in deal(): fail first, then remove.
"""

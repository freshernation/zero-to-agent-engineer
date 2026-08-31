"""Week 4, Day 2 - dunders and composition.

Run me:  pytest week-04/day-2 -v
"""

import pytest


class TestPoint:
    def test_repr(self, load):
        Point = load("point.py").Point
        assert repr(Point(3, 4)) == "Point(3, 4)"
        assert repr(Point(0, -2)) == "Point(0, -2)", (
            "__repr__ should be built from the actual attributes, not hard-coded."
        )

    def test_repr_works_inside_a_list(self, load):
        Point = load("point.py").Point
        assert str([Point(1, 2)]) == "[Point(1, 2)]"

    def test_eq(self, load):
        Point = load("point.py").Point
        assert Point(3, 4) == Point(3, 4)
        assert not (Point(3, 4) == Point(3, 5))

    def test_eq_against_something_else(self, load):
        Point = load("point.py").Point
        assert not (Point(3, 4) == "not a point"), (
            "Comparing a Point to a string should be False, not a crash. "
            "Check isinstance and return NotImplemented."
        )

    def test_in_uses_eq(self, load):
        Point = load("point.py").Point
        assert Point(1, 1) in [Point(0, 0), Point(1, 1)]

    def test_distance_to(self, load):
        Point = load("point.py").Point
        assert Point(0, 0).distance_to(Point(3, 4)) == 5.0
        assert Point(1, 1).distance_to(Point(1, 1)) == 0.0
        assert Point(0, 0).distance_to(Point(1, 1)) == 1.41

    def test_move(self, load):
        Point = load("point.py").Point
        p = Point(1, 1)
        assert p.move(2, 3) is None
        assert p.x == 3 and p.y == 4


class TestExpense:
    def test_attributes(self, load):
        Expense = load("ledger.py").Expense
        e = Expense("Coffee", 4.5, "food")
        assert e.description == "Coffee"
        assert e.amount == 4.5
        assert e.category == "food"

    def test_repr_quotes_the_strings(self, load):
        Expense = load("ledger.py").Expense
        assert repr(Expense("Coffee", 4.5, "food")) == "Expense('Coffee', 4.5, 'food')", (
            "Use !r in the f-string - f'{self.description!r}' - and Python adds "
            "the quotes for you."
        )


class TestLedger:
    @pytest.fixture
    def stocked(self, load):
        mod = load("ledger.py")
        ledger = mod.Ledger()
        ledger.add(mod.Expense("Coffee", 4.5, "food"))
        ledger.add(mod.Expense("Bus", 2.0, "transport"))
        ledger.add(mod.Expense("Lunch", 11.25, "food"))
        return mod, ledger

    def test_starts_empty(self, load):
        ledger = load("ledger.py").Ledger()
        assert len(ledger) == 0
        assert ledger.total() == 0
        assert ledger.biggest() is None

    def test_len(self, stocked):
        _, ledger = stocked
        assert len(ledger) == 3

    def test_total(self, stocked):
        _, ledger = stocked
        assert ledger.total() == 17.75

    def test_by_category(self, stocked):
        _, ledger = stocked
        food = ledger.by_category("food")
        assert len(food) == 2
        assert [e.description for e in food] == ["Coffee", "Lunch"]
        assert ledger.by_category("nothing") == []

    def test_biggest_returns_the_expense_itself(self, stocked):
        _, ledger = stocked
        biggest = ledger.biggest()
        assert biggest.description == "Lunch", (
            "biggest() returns the Expense object, not its amount or its name."
        )

    def test_repr(self, stocked):
        _, ledger = stocked
        assert repr(ledger) == "Ledger(3 expenses, $17.75)"


class TestCard:
    def test_repr(self, load):
        Card = load("deck.py").Card
        assert repr(Card("A", "spades")) == "Card('A', 'spades')"

    def test_eq(self, load):
        Card = load("deck.py").Card
        assert Card("A", "spades") == Card("A", "spades")
        assert not (Card("A", "spades") == Card("A", "hearts"))


class TestDeck:
    @pytest.fixture
    def five(self, load):
        mod = load("deck.py")
        cards = [mod.Card(str(n), "spades") for n in range(1, 6)]
        return mod, mod.Deck(cards)

    def test_len(self, five):
        _, deck = five
        assert len(deck) == 5

    def test_repr(self, five):
        _, deck = five
        assert repr(deck) == "Deck(5 cards)"

    def test_deal_returns_the_top_cards(self, five):
        mod, deck = five
        dealt = deck.deal(2)
        assert dealt == [mod.Card("1", "spades"), mod.Card("2", "spades")]

    def test_deal_removes_them(self, five):
        _, deck = five
        deck.deal(2)
        assert len(deck) == 3

    def test_deal_everything(self, five):
        _, deck = five
        assert len(deck.deal(5)) == 5
        assert len(deck) == 0

    def test_deal_too_many_leaves_the_deck_alone(self, five):
        _, deck = five
        with pytest.raises(ValueError) as caught:
            deck.deal(6)
        assert "Not enough cards" in str(caught.value)
        assert len(deck) == 5, (
            "The failed deal removed cards anyway. Check the count BEFORE you "
            "take any - fail first, then act."
        )

    def test_add_goes_on_the_bottom(self, five):
        mod, deck = five
        deck.add(mod.Card("K", "hearts"))
        assert len(deck) == 6
        assert deck.deal(1) == [mod.Card("1", "spades")], (
            "add() puts a card on the bottom, so the next deal is unaffected."
        )

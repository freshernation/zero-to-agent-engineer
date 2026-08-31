"""Week 4, Day 1 - classes.

Run me:  pytest week-04/day-1 -v
"""

import pytest


class TestRectangle:
    def test_attributes(self, load):
        R = load("rectangle.py").Rectangle
        r = R(3, 4)
        assert r.width == 3
        assert r.height == 4

    def test_area_and_perimeter(self, load):
        R = load("rectangle.py").Rectangle
        assert R(3, 4).area() == 12
        assert R(3, 4).perimeter() == 14
        assert R(5, 5).area() == 25

    def test_is_square(self, load):
        R = load("rectangle.py").Rectangle
        assert R(4, 4).is_square() is True
        assert R(3, 4).is_square() is False

    def test_scale_changes_the_instance(self, load):
        R = load("rectangle.py").Rectangle
        r = R(3, 4)
        result = r.scale(2)
        assert r.width == 6 and r.height == 8, (
            f"After scale(2) the sides should be 6 and 8, got {r.width} and "
            f"{r.height}. A method that changes its own instance uses self."
        )
        assert result is None, (
            "scale() changes the rectangle rather than returning a new one, "
            "so it should not return anything."
        )

    def test_instances_are_independent(self, load):
        R = load("rectangle.py").Rectangle
        a, b = R(1, 1), R(2, 2)
        a.scale(10)
        assert b.width == 2, (
            "Scaling one rectangle changed another. Attributes set in __init__ "
            "with self belong to one instance; a value set on the class itself "
            "is shared by all of them."
        )


class TestBankAccount:
    def test_starts_with_the_right_balance(self, load):
        Account = load("account.py").BankAccount
        assert Account("Ana").balance == 0
        assert Account("Ana", 100).balance == 100
        assert Account("Ana", 100).owner == "Ana"

    def test_deposit(self, load):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        a.deposit(50)
        assert a.balance == 150

    @pytest.mark.parametrize("bad", [0, -1, -100])
    def test_deposit_rejects_nonpositive(self, load, bad):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        with pytest.raises(ValueError) as caught:
            a.deposit(bad)
        assert "Deposit must be positive" in str(caught.value)
        assert a.balance == 100, (
            "A refused deposit changed the balance anyway. Check the amount "
            "before you apply it - an object that half-applies a change is "
            "worse than one that refuses."
        )

    def test_withdraw(self, load):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        a.withdraw(30)
        assert a.balance == 70

    def test_withdraw_everything_is_allowed(self, load):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        a.withdraw(100)
        assert a.balance == 0

    def test_withdraw_too_much(self, load):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        with pytest.raises(ValueError) as caught:
            a.withdraw(101)
        assert "Insufficient funds" in str(caught.value)
        assert a.balance == 100

    def test_can_afford(self, load):
        Account = load("account.py").BankAccount
        a = Account("Ana", 100)
        assert a.can_afford(100) is True
        assert a.can_afford(101) is False
        assert a.balance == 100, "can_afford should not change anything."


class TestInventory:
    def test_starts_empty(self, load):
        inv = load("inventory.py").Inventory()
        assert inv.is_empty() is True
        assert inv.total_items() == 0
        assert inv.quantity_of("Widget") == 0

    def test_add(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 3)
        assert inv.quantity_of("Widget") == 3
        assert inv.is_empty() is False

    def test_add_tops_up(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 3)
        inv.add("Widget", 2)
        assert inv.quantity_of("Widget") == 5

    def test_total_items(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 3)
        inv.add("Gadget", 4)
        assert inv.total_items() == 7

    def test_remove(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 5)
        inv.remove("Widget", 2)
        assert inv.quantity_of("Widget") == 3

    def test_remove_too_many_names_the_item(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 1)
        with pytest.raises(ValueError) as caught:
            inv.remove("Widget", 2)
        assert "Not enough Widget" in str(caught.value), (
            f"Expected the message to name the item, got '{caught.value}'."
        )
        assert inv.quantity_of("Widget") == 1

    def test_remove_something_never_added(self, load):
        inv = load("inventory.py").Inventory()
        with pytest.raises(ValueError):
            inv.remove("Ghost", 1)

    def test_empty_again_after_removing_everything(self, load):
        inv = load("inventory.py").Inventory()
        inv.add("Widget", 2)
        inv.remove("Widget", 2)
        assert inv.is_empty() is True

    def test_two_inventories_are_separate(self, load):
        Inventory = load("inventory.py").Inventory
        a, b = Inventory(), Inventory()
        a.add("Widget", 5)
        assert b.total_items() == 0, (
            "Adding to one inventory changed another. Build the storage inside "
            "__init__ with self, not as a value on the class."
        )

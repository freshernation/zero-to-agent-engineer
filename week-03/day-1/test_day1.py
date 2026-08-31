"""Week 3, Day 1 - functions.

Run me:  pytest week-03/day-1 -v

These tests import your file and call your functions. A function that prints its
answer instead of returning it will fail every test here, which is the point.
"""

import pytest


class TestMoney:
    def test_add_tax_default_rate(self, load):
        money = load("money.py")
        assert money.add_tax(100) == 108.00
        assert money.add_tax(50) == 54.00

    def test_add_tax_custom_rate(self, load):
        money = load("money.py")
        assert money.add_tax(100, 0.20) == 120.00
        assert money.add_tax(100, rate=0.20) == 120.00

    def test_add_tax_rounds(self, load):
        money = load("money.py")
        assert money.add_tax(49.99) == 53.99

    def test_apply_discount(self, load):
        money = load("money.py")
        assert money.apply_discount(50, 10) == 45.00
        assert money.apply_discount(100, 25) == 75.00
        assert money.apply_discount(19.99, 25) == 14.99

    def test_split_bill(self, load):
        money = load("money.py")
        assert money.split_bill(100, 4) == 25.00
        assert money.split_bill(100, 3) == 33.33

    def test_functions_return_rather_than_print(self, load, capsys):
        money = load("money.py")
        result = money.add_tax(100)
        printed = capsys.readouterr().out
        assert result is not None, (
            "add_tax(100) handed back None. It printed the answer instead of "
            "returning it - see the 'return is not print' section of the README."
        )
        assert printed == "", (
            f"add_tax printed {printed!r}. A calculation function should return "
            "its answer silently and let the caller decide what to display."
        )

    def test_has_docstrings(self, load):
        money = load("money.py")
        for name in ["add_tax", "apply_discount", "split_bill"]:
            func = getattr(money, name)
            assert func.__doc__, f"{name}() needs a docstring saying what it returns."


class TestGrades:
    @pytest.mark.parametrize("score,grade", [
        (100, "A"), (90, "A"), (89, "B"), (80, "B"),
        (79, "C"), (70, "C"), (69, "D"), (60, "D"), (59, "F"), (0, "F"),
    ])
    def test_letter_grade(self, load, score, grade):
        assert load("grades.py").letter_grade(score) == grade

    def test_average(self, load):
        grades = load("grades.py")
        assert grades.average([90, 80, 70]) == 80.0
        assert grades.average([1, 2]) == 1.5
        assert grades.average([100]) == 100.0

    def test_highest(self, load):
        grades = load("grades.py")
        assert grades.highest([90, 80, 70]) == 90
        assert grades.highest([5]) == 5

    def test_count_passing_default(self, load):
        grades = load("grades.py")
        assert grades.count_passing([50, 60, 90]) == 2
        assert grades.count_passing([10, 20]) == 0

    def test_count_passing_custom_threshold(self, load):
        grades = load("grades.py")
        assert grades.count_passing([50, 60, 90], 70) == 1
        assert grades.count_passing([50, 60, 90], threshold=50) == 3


class TestLabels:
    def test_price_label(self, load):
        labels = load("labels.py")
        assert labels.price_label(4.5) == "$4.50"
        assert labels.price_label(12) == "$12.00"
        assert labels.price_label(0) == "$0.00"

    def test_initials(self, load):
        labels = load("labels.py")
        assert labels.initials("Ana", "Silva") == "A.S."
        assert labels.initials("Benjamin", "Okafor") == "B.O."

    def test_summary_line(self, load):
        labels = load("labels.py")
        assert labels.summary_line("Ana", 4.5) == "Ana          $4.50"
        assert labels.summary_line("Benjamin", 12) == "Benjamin     $12.00"

    def test_summary_line_calls_price_label(self, load):
        """Swap price_label out. If summary_line formats money itself, it
        will not notice - and that is the duplication we are avoiding."""
        labels = load("labels.py")
        labels._module.price_label = lambda amount: "XX"
        result = labels.summary_line("Ana", 4.5)
        assert "XX" in result, (
            "summary_line formatted the money itself instead of calling "
            "price_label(). Call it - then a change to the price format only "
            "has to happen in one place."
        )

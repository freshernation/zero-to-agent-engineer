"""Week 3 milestone - the expense tracker.

Run me:  pytest week-03/milestone -v

Most tests call expenses.py directly. The rest run tracker.py and type commands
into it, exactly the way a person would.
"""

import json
from pathlib import Path

import pytest

COFFEE = {"description": "Coffee", "amount": 4.5, "category": "food"}
BUS = {"description": "Bus", "amount": 2.0, "category": "transport"}
LUNCH = {"description": "Lunch", "amount": 11.25, "category": "food"}


@pytest.fixture(autouse=True)
def clean_save_file(request):
    """tracker.py saves next to itself. Clear it around every test."""
    save = Path(request.fspath).parent / "expenses.json"
    save.unlink(missing_ok=True)
    yield
    save.unlink(missing_ok=True)


class TestParseAmount:
    def test_valid(self, load):
        e = load("expenses.py")
        assert e.parse_amount("4.50") == 4.5
        assert e.parse_amount("10") == 10.0
        assert e.parse_amount("0") == 0.0

    def test_not_a_number(self, load):
        e = load("expenses.py")
        with pytest.raises(ValueError) as caught:
            e.parse_amount("abc")
        assert "Amount must be a number" in str(caught.value)

    def test_negative(self, load):
        e = load("expenses.py")
        with pytest.raises(ValueError) as caught:
            e.parse_amount("-5")
        assert "Amount cannot be negative" in str(caught.value)


class TestAddExpense:
    def test_adds_the_right_shape(self, load):
        e = load("expenses.py")
        result = e.add_expense([], "Coffee", 4.5, "food")
        assert result == [COFFEE], (
            f"Got {result}. An expense is a dict with exactly the keys "
            "description, amount and category."
        )

    def test_adds_to_the_end(self, load):
        e = load("expenses.py")
        result = e.add_expense([COFFEE], "Bus", 2.0, "transport")
        assert result == [COFFEE, BUS]

    def test_does_not_change_the_list_it_was_given(self, load):
        """The one that catches people. Take values in, hand new ones back."""
        e = load("expenses.py")
        original = []
        e.add_expense(original, "Coffee", 4.5, "food")
        assert original == [], (
            "add_expense modified the list it was handed. Build and return a new "
            "one - a function that quietly changes its arguments is the hardest "
            "kind of bug to find, because the caller has no idea it happened."
        )


class TestTotal:
    def test_sums(self, load):
        e = load("expenses.py")
        assert e.total([COFFEE, BUS]) == 6.5
        assert e.total([COFFEE, BUS, LUNCH]) == 17.75

    def test_empty(self, load):
        assert load("expenses.py").total([]) == 0

    def test_rounds(self, load):
        e = load("expenses.py")
        messy = [{"description": "a", "amount": 0.1, "category": "x"}] * 3
        assert e.total(messy) == 0.3, (
            "0.1 three times is 0.30000000000000004 in binary floating point. "
            "Round the total to 2 decimal places."
        )


class TestByCategory:
    def test_groups_and_sums(self, load):
        e = load("expenses.py")
        assert e.by_category([COFFEE, BUS, LUNCH]) == {
            "food": 15.75,
            "transport": 2.0,
        }

    def test_single_category(self, load):
        assert load("expenses.py").by_category([COFFEE]) == {"food": 4.5}

    def test_empty(self, load):
        assert load("expenses.py").by_category([]) == {}


class TestFormatExpense:
    def test_format(self, load):
        e = load("expenses.py")
        assert e.format_expense(COFFEE) == "Coffee              food        $    4.50"

    def test_long_description(self, load):
        e = load("expenses.py")
        expense = {
            "description": "Monthly train pass",
            "amount": 89.0,
            "category": "transport",
        }
        assert e.format_expense(expense) == (
            "Monthly train pass  transport   $   89.00"
        )

    def test_returns_rather_than_prints(self, load, capsys):
        e = load("expenses.py")
        result = e.format_expense(COFFEE)
        assert capsys.readouterr().out == "", (
            "format_expense printed. expenses.py never prints - it hands strings "
            "back and lets tracker.py decide what to do with them."
        )
        assert isinstance(result, str)


class TestStorage:
    def test_save_then_load(self, load, tmp_path):
        e = load("expenses.py")
        path = str(tmp_path / "e.json")
        e.save_expenses(path, [COFFEE, BUS])
        assert e.load_expenses(path) == [COFFEE, BUS]

    def test_saves_real_json(self, load, tmp_path):
        e = load("expenses.py")
        path = tmp_path / "e.json"
        e.save_expenses(str(path), [COFFEE])
        assert json.loads(path.read_text()) == [COFFEE]

    def test_missing_file(self, load, tmp_path):
        e = load("expenses.py")
        assert e.load_expenses(str(tmp_path / "nope.json")) == []

    def test_damaged_file(self, load, tmp_path):
        e = load("expenses.py")
        path = tmp_path / "broken.json"
        path.write_text("[{oh no")
        assert e.load_expenses(str(path)) == [], (
            "A damaged save file raises json.JSONDecodeError, not "
            "FileNotFoundError. Catch both - this is the failure that works "
            "fine until the day it does not."
        )


class TestLibraryIsClean:
    def test_no_printing_or_input(self, load, source):
        load("expenses.py").format_expense  # nothing to check until it exists
        code = source("expenses.py", code_only=True)
        assert "print(" not in code, (
            "expenses.py contains a print(). The library never displays "
            "anything - that is tracker.py's job, and it is what lets the same "
            "logic be used by a website or a test suite later."
        )
        assert "input(" not in code, (
            "expenses.py contains an input(). The library never asks questions."
        )


class TestTrackerAdd:
    def test_add_confirms(self, run):
        r = run("tracker.py", answers=["add", "Coffee", "4.50", "food", "quit"])
        r.expect("Added: Coffee $4.50 (food)")

    def test_add_then_list(self, run):
        r = run("tracker.py", answers=[
            "add", "Coffee", "4.50", "food",
            "add", "Bus", "2.00", "transport",
            "list", "quit",
        ])
        r.expect("Coffee              food        $    4.50")
        r.expect("Bus                 transport   $    2.00")

    def test_bad_amount_abandons_the_add(self, run):
        r = run("tracker.py", answers=["add", "Coffee", "abc", "list", "quit"])
        r.expect("Amount must be a number")
        r.expect("No expenses yet.")

    def test_negative_amount_abandons_the_add(self, run):
        r = run("tracker.py", answers=["add", "Refund", "-5", "list", "quit"])
        r.expect("Amount cannot be negative")
        r.expect("No expenses yet.")


class TestTrackerCommands:
    def test_total(self, run):
        r = run("tracker.py", answers=[
            "add", "Coffee", "4.50", "food",
            "add", "Bus", "2.00", "transport",
            "total", "quit",
        ])
        r.expect("Total: $6.50")

    def test_report_is_alphabetical(self, run):
        r = run("tracker.py", answers=[
            "add", "Bus", "2.00", "transport",
            "add", "Coffee", "4.50", "food",
            "report", "quit",
        ])
        r.expect("food        $    4.50")
        r.expect("transport   $    2.00")
        # these exact strings only occur in the report, so their positions
        # in the output tell us the order the categories came out in
        food = r.stdout.index("food        $    4.50")
        transport = r.stdout.index("transport   $    2.00")
        assert food < transport, (
            "The report listed transport before food. Sort the categories."
        )

    def test_empty_list_and_report(self, run):
        r = run("tracker.py", answers=["list", "report", "quit"])
        assert r.stdout.count("No expenses yet.") == 2

    def test_unknown_command(self, run):
        run("tracker.py", answers=["banana", "quit"]).expect(
            "Unknown command: banana"
        )

    def test_quit_counts_singular(self, run):
        r = run("tracker.py", answers=["add", "Coffee", "4.50", "food", "quit"])
        r.expect("Saved 1 expense.")

    def test_quit_counts_plural(self, run):
        r = run("tracker.py", answers=[
            "add", "Coffee", "4.50", "food",
            "add", "Bus", "2.00", "transport",
            "quit",
        ])
        r.expect("Saved 2 expenses.")

    def test_quit_with_nothing(self, run):
        run("tracker.py", answers=["quit"]).expect("Saved 0 expenses.")


class TestPersistence:
    def test_data_survives_a_restart(self, run):
        """The whole point of the week."""
        run("tracker.py", answers=["add", "Coffee", "4.50", "food", "quit"])
        second = run("tracker.py", answers=["list", "total", "quit"])
        second.expect("Coffee              food        $    4.50")
        second.expect("Total: $4.50")
        second.expect("Saved 1 expense.")

    def test_survives_a_damaged_save_file(self, run, request):
        save = Path(request.fspath).parent / "expenses.json"
        save.write_text("[{ruined")
        r = run("tracker.py", answers=["list", "quit"])
        r.expect("No expenses yet.")

    def test_tracker_uses_the_library(self, source):
        code = source("tracker.py", code_only=True)
        assert "expenses" in code, (
            "tracker.py should import expenses.py and use it, not reimplement "
            "the logic."
        )
        assert "import json" not in code and "json.dump" not in code, (
            "tracker.py should not touch JSON directly - load_expenses and "
            "save_expenses in the library do that. (Naming the save file "
            "expenses.json is fine.)"
        )

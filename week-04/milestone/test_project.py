"""Project 1 - the expense tracker.

Run me:  pytest week-04/milestone -v

Three kinds of test in here:
  * does your code work
  * would your test suite notice if it did not
  * is the README finished
"""

import ast
import json
from pathlib import Path

import pytest

# Implementations with the right shape and no behaviour. A real test suite
# must fail against both. Neither shows you how to write the real thing.
DEAD = '''
class Ledger:
    def __init__(self): pass
    def add(self, expense): pass
    def total(self): pass
    def by_category(self, category): pass
    def categories(self): pass
    def biggest(self): pass
    def __len__(self): return 0
    def __repr__(self): return ""
    def save(self, path): pass

def load_ledger(path): return Ledger()
'''

HOLLOW = '''
class Ledger:
    def __init__(self): self.expenses = []
    def add(self, expense): self.expenses.append(expense)
    def total(self): return 0.0
    def by_category(self, category): return []
    def categories(self): return []
    def biggest(self): return None
    def __len__(self): return len(self.expenses)
    def __repr__(self): return "Ledger(0 expenses, $0.00)"
    def save(self, path): pass

def load_ledger(path): return Ledger()
'''


@pytest.fixture(autouse=True)
def clean_save_file(request):
    save = Path(request.fspath).parent / "expenses.json"
    save.unlink(missing_ok=True)
    yield
    save.unlink(missing_ok=True)


@pytest.fixture
def make(load):
    """Build Expenses and a stocked Ledger from the student's own classes."""
    Expense = load("expense.py").Expense
    mod = load("ledger.py")

    def _make():
        ledger = mod.Ledger()
        items = [
            Expense("Coffee", 4.5, "food"),
            Expense("Bus", 2.0, "transport"),
            Expense("Lunch", 11.25, "food"),
        ]
        for item in items:
            ledger.add(item)
        return mod, Expense, ledger, items

    return _make


class TestExpense:
    def test_attributes(self, load):
        e = load("expense.py").Expense("Coffee", 4.5, "food")
        assert (e.description, e.amount, e.category) == ("Coffee", 4.5, "food")

    def test_rejects_empty_description(self, load):
        Expense = load("expense.py").Expense
        with pytest.raises(ValueError) as caught:
            Expense("", 4.5, "food")
        assert "Description cannot be empty" in str(caught.value)

    @pytest.mark.parametrize("bad", [0, -1, -0.01])
    def test_rejects_non_positive_amount(self, load, bad):
        Expense = load("expense.py").Expense
        with pytest.raises(ValueError) as caught:
            Expense("Coffee", bad, "food")
        assert "Amount must be positive" in str(caught.value)

    def test_repr(self, load):
        Expense = load("expense.py").Expense
        assert repr(Expense("Coffee", 4.5, "food")) == "Expense('Coffee', 4.5, 'food')"

    def test_eq(self, load):
        Expense = load("expense.py").Expense
        assert Expense("Coffee", 4.5, "food") == Expense("Coffee", 4.5, "food")
        assert not (Expense("Coffee", 4.5, "food") == Expense("Tea", 4.5, "food"))
        assert not (Expense("Coffee", 4.5, "food") == "coffee")


class TestLedger:
    def test_starts_empty(self, load):
        ledger = load("ledger.py").Ledger()
        assert len(ledger) == 0
        assert ledger.total() == 0
        assert ledger.biggest() is None
        assert ledger.categories() == []

    def test_len_and_total(self, make):
        _, _, ledger, _ = make()
        assert len(ledger) == 3
        assert ledger.total() == 17.75

    def test_add_rejects_other_things(self, load):
        ledger = load("ledger.py").Ledger()
        with pytest.raises(TypeError) as caught:
            ledger.add({"description": "Coffee", "amount": 4.5})
        assert "Can only add Expense objects" in str(caught.value)
        assert len(ledger) == 0

    def test_by_category_keeps_order(self, make):
        _, _, ledger, items = make()
        food = ledger.by_category("food")
        assert [e.description for e in food] == ["Coffee", "Lunch"]
        assert ledger.by_category("nothing") == []

    def test_categories_sorted_and_unique(self, make):
        _, _, ledger, _ = make()
        assert ledger.categories() == ["food", "transport"]

    def test_biggest(self, make):
        _, _, ledger, _ = make()
        assert ledger.biggest().description == "Lunch"

    def test_repr(self, make):
        _, _, ledger, _ = make()
        assert repr(ledger) == "Ledger(3 expenses, $17.75)"


class TestPersistence:
    def test_save_and_load(self, make, tmp_path):
        mod, _, ledger, _ = make()
        path = str(tmp_path / "e.json")
        ledger.save(path)
        again = mod.load_ledger(path)
        assert len(again) == 3
        assert again.total() == 17.75
        assert again.categories() == ["food", "transport"]

    def test_saves_real_json(self, make, tmp_path):
        _, _, ledger, _ = make()
        path = tmp_path / "e.json"
        ledger.save(str(path))
        json.loads(path.read_text())

    def test_missing_file(self, load, tmp_path):
        mod = load("ledger.py")
        assert len(mod.load_ledger(str(tmp_path / "nope.json"))) == 0

    def test_damaged_file(self, load, tmp_path):
        mod = load("ledger.py")
        path = tmp_path / "bad.json"
        path.write_text("[{ruined")
        assert len(mod.load_ledger(str(path))) == 0


class TestLibrariesStayClean:
    @pytest.mark.parametrize("name", ["expense.py", "ledger.py"])
    def test_no_printing_or_input(self, load, source, name):
        module = load(name)
        module.Expense if name == "expense.py" else module.Ledger
        code = source(name, code_only=True)
        assert "print(" not in code, f"{name} contains a print(). That is cli.py's job."
        assert "input(" not in code, f"{name} contains an input(). That is cli.py's job."


class TestCli:
    def test_add_and_list(self, run):
        r = run("cli.py", answers=[
            "add", "Coffee", "4.50", "food",
            "add", "Bus", "2.00", "transport",
            "list", "quit",
        ])
        r.expect("Added: Coffee $4.50 (food)")
        r.expect("Coffee              food        $    4.50")
        r.expect("Bus                 transport   $    2.00")

    def test_total_and_report(self, run):
        r = run("cli.py", answers=[
            "add", "Coffee", "4.50", "food",
            "add", "Bus", "2.00", "transport",
            "total", "report", "quit",
        ])
        r.expect("Total: $6.50")
        r.expect("food        $    4.50")
        r.expect("transport   $    2.00")

    def test_rejects_bad_amount(self, run):
        r = run("cli.py", answers=["add", "Coffee", "-5", "food", "list", "quit"])
        r.expect("Amount must be positive")
        r.expect("No expenses yet.")

    def test_rejects_empty_description(self, run):
        r = run("cli.py", answers=["add", "", "4.50", "food", "list", "quit"])
        r.expect("Description cannot be empty")
        r.expect("No expenses yet.")

    def test_unknown_command(self, run):
        run("cli.py", answers=["banana", "quit"]).expect("Unknown command: banana")

    def test_quit_counts(self, run):
        run("cli.py", answers=["quit"]).expect("Saved 0 expenses.")
        run("cli.py", answers=["add", "Coffee", "4.50", "food", "quit"]).expect(
            "Saved 1 expense."
        )

    def test_data_survives_a_restart(self, run):
        run("cli.py", answers=["add", "Coffee", "4.50", "food", "quit"])
        r = run("cli.py", answers=["total", "quit"])
        r.expect("Total: $4.50")


class TestYourTestSuite:
    def test_it_passes_on_your_own_code(self, run_tests_against, source):
        result = run_tests_against(
            "test_ledger.py", {}, also_copy=["expense.py", "ledger.py"]
        )
        assert result.passed, (
            "Your own suite does not pass against your own code.\n\n"
            + result.output[-2000:]
        )

    def test_it_fails_when_nothing_works(self, run_tests_against):
        result = run_tests_against(
            "test_ledger.py", {"ledger.py": DEAD}, also_copy=["expense.py"]
        )
        assert not result.no_tests, (
            "test_ledger.py contains no tests yet, so it did not catch anything. "
            "Write the suite first."
        )
        assert not result.no_tests, (
            "test_ledger.py contains no tests yet, so it did not catch anything. "
            "Write the suite first."
        )
        assert not result.passed, (
            "\nYour suite passed against a Ledger whose every method does "
            "nothing at all.\n\n"
            "That means none of your tests checks a result. A suite that goes "
            "green on code that does nothing has not tested anything - it has "
            "just run some code."
        )

    def test_it_fails_on_plausible_constants(self, run_tests_against):
        result = run_tests_against(
            "test_ledger.py", {"ledger.py": HOLLOW}, also_copy=["expense.py"]
        )
        assert not result.no_tests, (
            "test_ledger.py contains no tests yet, so it did not catch anything. "
            "Write the suite first."
        )
        assert not result.no_tests, (
            "test_ledger.py contains no tests yet, so it did not catch anything. "
            "Write the suite first."
        )
        assert not result.passed, (
            "\nYour suite passed against a Ledger where total() always returns "
            "0.0, by_category() always returns [], categories() is always empty "
            "and add() validates nothing.\n\n"
            "Which of those would your tests have caught? Add one test for each."
        )

    def test_enough_tests(self, source):
        tree = ast.parse(source("test_ledger.py"))
        tests = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        assert len(tests) >= 12, (
            f"Found {len(tests)} test functions, expected at least 12."
        )

    def test_covers_the_error_paths(self, source):
        code = source("test_ledger.py")
        assert code.count("pytest.raises") >= 2, (
            "At least two pytest.raises. There are three different refusals in "
            "this project - the empty description, the bad amount, and adding "
            "something that is not an Expense."
        )

    def test_uses_parametrize(self, source):
        code = source("test_ledger.py")
        assert "def test_" in code, "test_ledger.py contains no tests yet."
        assert "parametrize" in code, (
            "No @pytest.mark.parametrize anywhere."
        )


class TestProjectReadme:
    HEADINGS = [
        "What it is",
        "What it does",
        "How to run it",
        "How to run the tests",
        "What I would do next",
    ]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_has_the_section(self, source, heading):
        text = source("PROJECT_README.md")
        assert f"## {heading}" in text, (
            f"PROJECT_README.md has no '{heading}' section."
        )
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 15, (
            f"The '{heading}' section is empty (or nearly). It needs at least a "
            "couple of real sentences - this is the only part of your project "
            "most people will ever read."
        )

    def test_is_actually_written(self, source):
        text = source("PROJECT_README.md")
        body = text.replace("<!--", "").split("-->")[-1]
        for heading in self.HEADINGS:
            body = body.replace(f"## {heading}", "")
        words = len(body.split())
        assert words >= 150, (
            f"PROJECT_README.md is {words} words of actual content, expected at "
            "least 150. This is the only thing most people will ever read."
        )

    def test_title_was_changed(self, source):
        assert "[Your project name]" not in source("PROJECT_README.md"), (
            "Give the project a real name at the top."
        )

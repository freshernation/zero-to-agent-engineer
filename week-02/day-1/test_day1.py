"""Week 2, Day 1 - lists.

Run me:  pytest week-02/day-1 -v
"""

import pytest


class TestRoster:
    def test_all_five_lines(self, run):
        r = run("roster.py")
        r.expect("First: Ana")
        r.expect("Last: Eve")
        r.expect("Third: Cara")
        r.expect("Count: 5")
        r.expect("Has Ben: True")

    def test_last_is_not_hard_coded(self, run, source):
        """The list gets longer on Friday. Position 4 will not be the end any more."""
        run("roster.py").require_output()
        code = source("roster.py", code_only=True)
        body = code.split("]", 1)[1] if "]" in code else code
        for bad in ["[4]", "[ 4 ]", "[5]"]:
            assert bad not in body, (
                f"Found {bad} in your code. Get the last item with names[-1] or "
                "len(names) - 1, so it still works when the list changes length."
            )


class TestSlices:
    def test_first_three(self, run):
        run("slices.py").expect("First three: [10, 20, 30]")

    def test_last_three(self, run):
        run("slices.py").expect("Last three: [60, 70, 80]")

    def test_every_other(self, run):
        run("slices.py").expect("Every other: [10, 30, 50, 70]")

    def test_backwards(self, run):
        run("slices.py").expect(
            "Backwards: [80, 70, 60, 50, 40, 30, 20, 10]"
        )

    def test_used_slicing_not_retyping(self, run, source):
        run("slices.py").require_output()
        code = source("slices.py", code_only=True)
        after_data = code.split("]", 1)[1] if "]" in code else code
        assert "20, 30" not in after_data, (
            "Do not retype the numbers. Take slices of the list you were given - "
            "that is the whole exercise."
        )


class TestBasket:
    def test_builds_and_edits_the_list(self, run):
        r = run("basket.py", answers=["apple", "milk", "eggs"])
        r.expect("Basket: ['milk', 'eggs', 'bread']")
        r.expect("Items: 3")

    @pytest.mark.parametrize("items", [
        ["rice", "beans", "salt"],
        ["tea", "jam", "oats"],
    ])
    def test_works_for_any_input(self, run, items):
        r = run("basket.py", answers=items)
        expected = [items[1], items[2], "bread"]
        r.expect(f"Basket: {expected}")
        r.expect("Items: 3")

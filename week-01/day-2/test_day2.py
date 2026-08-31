"""Day 2 - variables, input, conversion, f-strings.

Run me:  pytest week-01/day-2 -v

These scripts ask questions, so the tests type answers into them. If a test says
your program is still running, check that your input() calls are in the order the
task listed.
"""

import pytest


class TestGreet:
    @pytest.mark.parametrize("name", ["Sam", "Priya", "Jo"])
    def test_greets_by_name(self, run, name):
        run("greet.py", answers=[name]).expect(f"Hello, {name}! Welcome to Python.")


class TestAge:
    @pytest.mark.parametrize("born,age", [(1990, 36), (2000, 26), (1975, 51)])
    def test_computes_age(self, run, born, age):
        run("age.py", answers=[born]).expect(f"You are {age} years old.")

    def test_year_is_not_hard_coded_into_the_maths(self, source):
        text = source("age.py", code_only=True)
        assert "2026" in text, "Store the current year (2026) in a variable."


class TestConvert:
    @pytest.mark.parametrize("c,f", [
        ("37", "37.0C = 98.6F"),
        ("100", "100.0C = 212.0F"),
        ("0", "0.0C = 32.0F"),
        ("-40", "-40.0C = -40.0F"),
    ])
    def test_converts(self, run, c, f):
        run("convert.py", answers=[c]).expect(f)


class TestCheckout:
    def test_simple_case(self, run):
        r = run("checkout.py", answers=["12.50", "2"])
        r.expect("Subtotal: $25.00")
        r.expect("Tax: $2.00")
        r.expect("Total: $27.00")

    def test_awkward_case(self, run):
        r = run("checkout.py", answers=["9.99", "3"])
        r.expect("Subtotal: $29.97")
        r.expect("Tax: $2.40")
        r.expect("Total: $32.37")

    def test_single_item(self, run):
        r = run("checkout.py", answers=["100", "1"])
        r.expect("Subtotal: $100.00")
        r.expect("Tax: $8.00")
        r.expect("Total: $108.00")

    def test_tax_rate_is_a_variable(self, source):
        text = source("checkout.py", code_only=True)
        assert "0.08" in text, (
            "Store the tax rate (0.08) in a variable rather than writing 8 percent "
            "as a magic number in the middle of a calculation."
        )

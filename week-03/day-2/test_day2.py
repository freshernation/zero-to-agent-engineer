"""Week 3, Day 2 - exceptions.

Run me:  pytest week-03/day-2 -v

`pytest.raises(...)` below is the test-writer's way of saying "this line SHOULD
blow up, and with this message". You do not need to write these yourself yet.
"""

import pytest


class TestSafe:
    def test_to_int_good_input(self, load):
        safe = load("safe.py")
        assert safe.to_int("42") == 42
        assert safe.to_int("0") == 0
        assert safe.to_int("-7") == -7

    def test_to_int_bad_input_uses_default(self, load):
        safe = load("safe.py")
        assert safe.to_int("abc") == 0
        assert safe.to_int("") == 0
        assert safe.to_int("4.5") == 0

    def test_to_int_custom_default(self, load):
        safe = load("safe.py")
        assert safe.to_int("abc", -1) == -1
        assert safe.to_int("abc", default=99) == 99

    def test_to_float(self, load):
        safe = load("safe.py")
        assert safe.to_float("4.5") == 4.5
        assert safe.to_float("10") == 10.0
        assert safe.to_float("abc") == 0.0
        assert safe.to_float("abc", -1.5) == -1.5

    def test_safe_divide(self, load):
        safe = load("safe.py")
        assert safe.safe_divide(10, 2) == 5.0
        assert safe.safe_divide(7, 2) == 3.5
        assert safe.safe_divide(10, 0) is None

    def test_no_bare_except(self, load, source):
        load("safe.py").to_int  # nothing to check until it exists
        code = source("safe.py", code_only=True)
        for line in code.splitlines():
            stripped = line.strip()
            assert stripped not in ("except:", "except Exception:"), (
                f"Found `{stripped}`. Catch the specific exception you expect - "
                "ValueError or ZeroDivisionError here. A bare except also "
                "swallows your own typos, and then the program does the wrong "
                "thing without telling you."
            )


class TestValidateAge:
    def test_valid_ages(self, load):
        validate = load("validate.py")
        assert validate.parse_age("30") == 30
        assert validate.parse_age("0") == 0
        assert validate.parse_age("130") == 130

    def test_not_a_number(self, load):
        validate = load("validate.py")
        with pytest.raises(ValueError) as caught:
            validate.parse_age("abc")
        assert "Age must be a whole number" in str(caught.value), (
            f"Expected the message 'Age must be a whole number', "
            f"got '{caught.value}'. Python's own ValueError from int() is not "
            "readable enough to show a person - catch it and raise your own."
        )

    @pytest.mark.parametrize("text", ["-5", "200", "131", "-1"])
    def test_out_of_range(self, load, text):
        validate = load("validate.py")
        with pytest.raises(ValueError) as caught:
            validate.parse_age(text)
        assert "Age must be between 0 and 130" in str(caught.value)


class TestValidateAmount:
    def test_valid_amounts(self, load):
        validate = load("validate.py")
        assert validate.parse_amount("4.50") == 4.5
        assert validate.parse_amount("10") == 10.0
        assert validate.parse_amount("0") == 0.0

    def test_not_a_number(self, load):
        validate = load("validate.py")
        with pytest.raises(ValueError) as caught:
            validate.parse_amount("abc")
        assert "Amount must be a number" in str(caught.value)

    def test_negative(self, load):
        validate = load("validate.py")
        with pytest.raises(ValueError) as caught:
            validate.parse_amount("-3")
        assert "Amount cannot be negative" in str(caught.value)


class TestAsk:
    def test_accepts_a_good_age_immediately(self, run):
        run("ask.py", answers=["30"]).expect("Thanks, you are 30.")

    def test_rejects_junk_then_accepts(self, run):
        r = run("ask.py", answers=["abc", "30"])
        r.expect("That is not a number. Try again.")
        r.expect("Thanks, you are 30.")

    def test_rejects_out_of_range_then_accepts(self, run):
        r = run("ask.py", answers=["200", "30"])
        r.expect("Age must be between 0 and 130. Try again.")
        r.expect("Thanks, you are 30.")

    def test_keeps_asking(self, run):
        r = run("ask.py", answers=["abc", "200", "-4", "45"])
        assert r.stdout.count("Try again") == 3, (
            "Three bad answers should produce three complaints. "
            f"Yours produced {r.stdout.count('Try again')}."
        )
        r.expect("Thanks, you are 45.")

"""Week 2, Day 3 - dicts, nested data, aligned output.

Run me:  pytest week-02/day-3 -v
"""

import pytest

TABLE = [
    "NAME         SCORE",
    "------------------",
    "Ana             92",
    "Benjamin        78",
    "Cara            85",
    "Dev             65",
    "------------------",
    "Average:      80.0",
]


class TestContact:
    def test_prints_the_three_fields(self, run):
        r = run("contact.py")
        r.expect("Name: Ana Silva")
        r.expect("Email: ana@example.com")
        r.expect("City: Lisbon")

    def test_adds_phone(self, run):
        r = run("contact.py")
        r.expect("Fields: 4")
        r.expect("Phone: 555-0182")

    def test_checks_a_missing_key(self, run):
        run("contact.py").expect("Has fax: False")


class TestCounts:
    def test_counts_in_alphabetical_order(self, run):
        r = run("counts.py")
        assert r.lines == ["apple: 3", "banana: 2", "cherry: 1"], (
            "Expected the three counts in alphabetical order, got:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_counts_are_not_hard_coded(self, run, source):
        run("counts.py").require_output()
        code = source("counts.py", code_only=True)
        after_data = code.split("]", 1)[1] if "]" in code else code
        for bad in ["3", "2", "1"]:
            assert f": {bad}" not in after_data.replace(" ", " "), (
                "Do not type the counts in. Count them with a loop and a dict."
            )


class TestLookup:
    @pytest.mark.parametrize("country,capital", [
        ("France", "Paris"),
        ("Japan", "Tokyo"),
        ("Brazil", "Brasilia"),
        ("Kenya", "Nairobi"),
    ])
    def test_known_countries(self, run, country, capital):
        run("lookup.py", answers=[country]).expect(f"Capital: {capital}")

    @pytest.mark.parametrize("country", ["Narnia", "", "france"])
    def test_unknown_countries_do_not_crash(self, run, country):
        r = run("lookup.py", answers=[country])
        r.expect("Capital: unknown")

    def test_uses_get(self, source):
        code = source("lookup.py", code_only=True)
        assert ".get(" in code, (
            "Use .get() with a default. An if/else works too, but .get() is the "
            "tool built for exactly this and you should have it in your hands."
        )


class TestRecords:
    def test_full_table(self, run):
        r = run("records.py")
        assert r.lines == TABLE, (
            "The table does not match. Expected:\n"
            + "\n".join(f"  | {ln}" for ln in TABLE)
            + "\n\nYours:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
            + "\n\nNames left-aligned in 12, scores right-aligned in 6."
        )

    def test_average_is_calculated(self, run, source):
        run("records.py").require_output()
        code = source("records.py", code_only=True)
        after_data = code.rsplit("]", 1)[-1]
        assert "80" not in after_data, (
            "Do not type 80 in. Add the scores up in a loop and divide by len()."
        )

"""Day 3 - conditionals.

Run me:  pytest week-01/day-3 -v

Most of these tests sit right on a boundary. That is deliberate: boundaries are
where conditional logic actually goes wrong, in this exercise and in production.
"""

import pytest


class TestGrade:
    @pytest.mark.parametrize("score,grade", [
        (100, "A"), (90, "A"),
        (89, "B"), (80, "B"),
        (79, "C"), (70, "C"),
        (69, "D"), (60, "D"),
        (59, "F"), (0, "F"),
    ])
    def test_grade_boundaries(self, run, score, grade):
        run("grade.py", answers=[score]).expect(f"Grade: {grade}")


class TestParity:
    @pytest.mark.parametrize("n,word", [
        (4, "even"), (7, "odd"), (0, "even"), (1, "odd"),
        (100, "even"), (-3, "odd"), (-8, "even"),
    ])
    def test_even_or_odd(self, run, n, word):
        r = run("parity.py", answers=[n])
        r.expect(word)
        wrong = "odd" if word == "even" else "even"
        assert wrong not in r.stdout, (
            f"{n} is {word}, but your program also printed '{wrong}'. "
            "Both branches ran - check your if/else."
        )


class TestLogin:
    def test_correct_credentials(self, run):
        run("login.py", answers=["admin", "python123"]).expect("Access granted.")

    @pytest.mark.parametrize("user,pw", [
        ("admin", "wrong"),
        ("wrong", "python123"),
        ("wrong", "wrong"),
        ("Admin", "python123"),
    ])
    def test_rejects_everything_else(self, run, user, pw):
        r = run("login.py", answers=[user, pw])
        r.expect("Access denied.")
        assert "granted" not in r.stdout, (
            f"Username {user!r} with password {pw!r} should be denied. "
            "Both parts have to be right - that is one 'and', not an 'or'."
        )


class TestTicket:
    @pytest.mark.parametrize("age,day,price", [
        (30, "Monday", "12.00"),      # standard
        (10, "Monday", "8.00"),       # child
        (70, "Monday", "9.00"),       # senior
        (12, "Monday", "8.00"),       # child boundary - 12 is still a child
        (13, "Monday", "12.00"),      # child boundary - 13 is not
        (65, "Monday", "9.00"),       # senior boundary - 65 counts
        (64, "Monday", "12.00"),      # senior boundary - 64 does not
        (30, "Tuesday", "10.00"),     # discount on standard
        (70, "Tuesday", "7.00"),      # discount on senior
        (12, "Tuesday", "6.00"),      # discount on child
        (30, "Wednesday", "12.00"),   # no discount on other days
    ])
    def test_pricing(self, run, age, day, price):
        run("ticket.py", answers=[age, day]).expect(f"Ticket: ${price}")

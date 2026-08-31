"""Week 2, Day 2 - loops.

Run me:  pytest week-02/day-2 -v
"""

import pytest


class TestCountdown:
    def test_exact_output(self, run):
        r = run("countdown.py")
        assert r.lines == ["10", "8", "6", "4", "2", "0", "Liftoff!"], (
            f"Expected 10 8 6 4 2 0 then Liftoff!, got:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_uses_a_loop(self, run, source):
        run("countdown.py").require_output()
        code = source("countdown.py", code_only=True)
        assert "range" in code, "Use range() and one loop, not seven print lines."
        assert code.count("print") <= 2, (
            f"You used {code.count('print')} print statements. "
            "One inside the loop and one for Liftoff! is all you need."
        )


class TestTotal:
    def test_prints_every_price(self, run):
        r = run("total.py")
        for price in ["$4.50", "$12.00", "$3.25", "$7.80", "$2.45"]:
            r.expect(price)

    def test_summary(self, run):
        r = run("total.py")
        r.expect("Total: $30.00")
        r.expect("Average: $6.00")
        r.expect("Highest: $12.00")
        r.expect("Lowest: $2.45")

    def test_total_is_accumulated_not_summed(self, run, source):
        run("total.py").require_output()
        code = source("total.py", code_only=True)
        assert "sum(" not in code, (
            "Build the total with an accumulator loop this time. "
            "You get to use sum() from tomorrow - today the point is knowing "
            "what it does for you."
        )

    def test_total_is_not_hard_coded(self, run, source):
        run("total.py").require_output()
        code = source("total.py", code_only=True)
        after_data = code.split("]", 1)[1] if "]" in code else code
        assert "30" not in after_data, (
            "Do not type the answer in. Work the total out from the list."
        )


class TestNumbered:
    def test_exact_output(self, run):
        r = run("numbered.py")
        assert r.lines == [
            "1. Write tests",
            "2. Fix the bug",
            "3. Push the branch",
        ], (
            "Expected the three tasks numbered from 1, got:\n"
            + "\n".join(f"  | {ln}" for ln in r.lines)
        )

    def test_uses_a_loop(self, run, source):
        run("numbered.py").require_output()
        code = source("numbered.py", code_only=True)
        after_data = code.split("]", 1)[1] if "]" in code else code
        assert "Fix the bug" not in after_data, (
            "Do not retype the tasks. Loop over the list you were given."
        )


class TestGuess:
    def test_three_guesses(self, run):
        r = run("guess.py", answers=[3, 9, 7])
        r.expect("Too low")
        r.expect("Too high")
        r.expect("Correct! It took 3 guesses.")

    def test_first_time(self, run):
        r = run("guess.py", answers=[7])
        r.expect("Correct! It took 1 guesses.")

    @pytest.mark.parametrize("guesses,count", [
        ([1, 2, 3, 4, 5, 6, 7], 7),
        ([10, 7], 2),
    ])
    def test_counts_every_guess(self, run, guesses, count):
        r = run("guess.py", answers=guesses)
        r.expect(f"Correct! It took {count} guesses.")

    def test_says_which_direction(self, run):
        r = run("guess.py", answers=[1, 7])
        assert "Too low" in r.stdout and "Too high" not in r.stdout, (
            "A guess of 1 against a secret of 7 is too low, and nothing else."
        )

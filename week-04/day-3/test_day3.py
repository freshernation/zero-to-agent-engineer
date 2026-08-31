"""Week 4, Day 3 - your tests get tested.

Run me:  pytest week-04/day-3 -v

The mutation tests below break shapes.py in six ways and run YOUR suite against
each broken version. A suite that still passes has not tested that behaviour.
"""

import ast
import pytest

# Each mutation is a real bug someone could plausibly write.
MUTATIONS = {
    "Circle.area returns the circumference formula": {
        "return round(PI * self.radius * self.radius, 2)":
        "return round(2 * PI * self.radius, 2)",
    },
    "Circle stops rejecting a radius of zero or less": {
        '        if radius <= 0:\n            raise ValueError("Radius must be positive")\n':
        "",
    },
    "Square.perimeter returns three times the side": {
        "return 4 * self.side": "return 3 * self.side",
    },
    "total_area quietly ignores the last shape": {
        "return round(sum(shape.area() for shape in shapes), 2)":
        "return round(sum(shape.area() for shape in shapes[:-1]), 2)",
    },
    "largest returns the smallest shape": {
        "return max(shapes, key=lambda shape: shape.area())":
        "return min(shapes, key=lambda shape: shape.area())",
    },
    "largest crashes on an empty list": {
        "    if not shapes:\n        return None\n": "",
    },
}


def _require_written(code, name):
    """These checks are about HOW a suite is written - meaningless before there
    is one."""
    if "def test_" not in code:
        pytest.fail(f"{name} contains no tests yet.")


def _tree(source, name):
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        pytest.fail(f"{name} does not parse: {exc}")


class TestYourShapeSuiteIsReal:
    def test_it_passes_on_the_correct_code(self, run_student_tests):
        result = run_student_tests("test_shapes.py", "shapes.py")
        assert result.passed, (
            "Your own test suite does not pass against the correct shapes.py.\n"
            "Fix that before worrying about anything else.\n\n"
            + result.output[-2000:]
        )

    @pytest.mark.parametrize("description", list(MUTATIONS))
    def test_it_catches_the_planted_bug(self, run_student_tests, description):
        result = run_student_tests(
            "test_shapes.py", "shapes.py", MUTATIONS[description]
        )
        assert not result.no_tests, (
            "test_shapes.py contains no tests yet, so of course it did not "
            "catch anything. Write the suite first."
        )
        assert not result.passed, (
            f"\nA bug was planted -- {description} -- and your suite still "
            f"passed.\n\n"
            "That means nothing you wrote would have caught it. A test suite "
            "that goes green on broken code is worse than no tests, because it "
            "produces confidence with nothing behind it.\n\n"
            "Add a test that would fail if this were true."
        )


class TestYourShapeSuiteIsWellBuilt:
    def test_has_enough_tests(self, source):
        tree = _tree(source("test_shapes.py"), "test_shapes.py")
        tests = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        assert len(tests) >= 8, (
            f"Found {len(tests)} test functions, expected at least 8."
        )

    def test_uses_pytest_raises(self, source):
        code = source("test_shapes.py")
        _require_written(code, "test_shapes.py")
        assert "pytest.raises" in code, (
            "No pytest.raises anywhere. The error paths are code too, and they "
            "are the least exercised part of any program."
        )

    def test_uses_parametrize(self, source):
        code = source("test_shapes.py")
        _require_written(code, "test_shapes.py")
        assert "parametrize" in code, (
            "No @pytest.mark.parametrize. Use it for at least one thing - the "
            "same test across several values is exactly what catches the "
            "area/circumference trap."
        )

    def test_did_not_change_shapes(self, source):
        _require_written(source("test_shapes.py"), "test_shapes.py")
        code = source("shapes.py")
        assert "return round(PI * self.radius * self.radius, 2)" in code, (
            "shapes.py has been modified. It is correct as given - today is "
            "about testing it, not changing it."
        )


class TestStats:
    def test_mean(self, load):
        stats = load("stats.py")
        assert stats.mean([1, 2, 3]) == 2.0
        assert stats.mean([10]) == 10.0
        assert stats.mean([1, 2]) == 1.5

    def test_mean_rounds(self, load):
        assert load("stats.py").mean([1, 1, 2]) == 1.33

    def test_mean_of_nothing(self, load):
        with pytest.raises(ValueError) as caught:
            load("stats.py").mean([])
        assert "No numbers" in str(caught.value)

    def test_median_sorts_first(self, load):
        stats = load("stats.py")
        assert stats.median([1, 3, 2]) == 2
        assert stats.median([9, 1, 5]) == 5

    def test_median_of_an_even_count(self, load):
        stats = load("stats.py")
        assert stats.median([1, 2, 3, 4]) == 2.5
        assert stats.median([4, 1]) == 2.5

    def test_median_of_nothing(self, load):
        with pytest.raises(ValueError):
            load("stats.py").median([])

    def test_mode(self, load):
        stats = load("stats.py")
        assert stats.mode([1, 2, 2, 3]) == 2
        assert stats.mode([5]) == 5

    def test_mode_breaks_ties_with_the_smallest(self, load):
        stats = load("stats.py")
        assert stats.mode([1, 1, 2, 2]) == 1
        assert stats.mode([3, 3, 1, 1]) == 1

    def test_spread(self, load):
        stats = load("stats.py")
        assert stats.spread([4, 1, 9]) == 8
        assert stats.spread([7]) == 0

    def test_you_wrote_tests_for_it(self, source):
        tree = _tree(source("test_stats.py"), "test_stats.py")
        tests = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        assert len(tests) >= 6, (
            f"test_stats.py has {len(tests)} test functions, expected at least 6. "
            "The point of today is writing them before the code, not after."
        )

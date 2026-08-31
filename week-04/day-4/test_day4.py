"""Week 4, Day 4 - type hints and class bugs.

Run me:  pytest week-04/day-4 -v
"""

import typing

import pytest

PLACEHOLDER = "(your answer)"


def hints(func):
    return getattr(func, "__annotations__", {})


class TestTypedBehaviour:
    def test_total(self, load):
        t = load("typed.py")
        assert t.total([1.5, 2.25]) == 3.75
        assert t.total([]) == 0

    def test_label(self, load):
        t = load("typed.py")
        assert t.label("Coffee", 4.5) == "Coffee: $4.50"

    def test_find(self, load):
        t = load("typed.py")
        assert t.find(["a", "b", "c"], "b") == 1
        assert t.find(["a"], "z") == -1
        assert t.find([], "z") == -1

    def test_first_match(self, load):
        t = load("typed.py")
        assert t.first_match(["Ana", "Ben", "Bea"], "B") == "Ben"
        assert t.first_match(["Ana"], "Z") is None

    def test_task(self, load):
        Task = load("typed.py").Task
        t = Task("Write tests")
        assert t.title == "Write tests"
        assert t.done is False
        assert t.summary() == "[ ] Write tests"
        assert t.complete() is None
        assert t.done is True
        assert t.summary() == "[x] Write tests"

    def test_task_can_start_done(self, load):
        Task = load("typed.py").Task
        assert Task("Ship it", True).summary() == "[x] Ship it"


class TestTypedAnnotations:
    @pytest.mark.parametrize("name,expected", [
        ("total", {"prices": list, "return": float}),
        ("label", {"name": str, "amount": float, "return": str}),
        ("find", {"names": list, "target": str, "return": int}),
    ])
    def test_function_hints(self, load, name, expected):
        func = getattr(load("typed.py"), name)
        actual = hints(func)
        for arg, want in expected.items():
            assert arg in actual, (
                f"{name}() has no type hint for '{arg}'. "
                f"Found: {actual or 'none at all'}"
            )
            assert actual[arg] is want, (
                f"{name}()'s '{arg}' is hinted as {actual[arg]}, expected {want.__name__}."
            )

    def test_first_match_is_optional(self, load):
        func = load("typed.py").first_match
        annotation = hints(func).get("return")
        assert annotation is not None, "first_match has no return type hint."
        assert annotation == typing.Optional[str], (
            f"first_match returns a name or None, so the hint is Optional[str]. "
            f"Yours says {annotation}."
        )

    def test_method_hints(self, load):
        Task = load("typed.py").Task
        init = hints(Task.__init__)
        assert init.get("title") is str, "Task.__init__ needs title: str"
        assert init.get("done") is bool, "Task.__init__ needs done: bool"
        assert init.get("return") is None, (
            "__init__ hands nothing back, so it is annotated -> None."
        )
        assert hints(Task.complete).get("return") is None
        assert hints(Task.summary).get("return") is str

    def test_self_is_not_annotated(self, load):
        Task = load("typed.py").Task
        assert "self" not in hints(Task.summary), (
            "Never annotate self - Python already knows what it is."
        )


class TestFixes:
    def test_broken_1_missing_self(self, run, source):
        run("broken_1.py").expect("Area: 12")
        code = source("broken_1.py", code_only=True)
        assert "def area(self)" in code.replace("  ", " "), (
            "The fix is to give area() its self parameter. r.area() is shorthand "
            "for Rectangle.area(r), so the instance always arrives as the first "
            "argument whether you named it or not."
        )

    def test_broken_2_shared_class_attribute(self, run):
        r = run("broken_2.py")
        r.expect("Ana: ['apple']")
        r.expect("Ben: []")

    def test_broken_2_basket_is_per_instance(self, run, source):
        run("broken_2.py").expect("Ben: []")
        code = source("broken_2.py", code_only=True)
        first_line = code.split("def __init__")[0]
        assert "basket = []" not in first_line, (
            "The basket is still declared on the class itself. A value set there "
            "is created once and shared by every instance - it has to be built "
            "in __init__ with self."
        )

    def test_broken_3_assigns_to_self(self, run, source):
        run("broken_3.py").expect("Total: 30")
        code = source("broken_3.py", code_only=True)
        assert "self.total" in code.split("def ring_up")[-1], (
            "ring_up has to assign to self.total. A plain `total = ...` makes a "
            "local variable that vanishes when the method ends - the same bug as "
            "week 3's add_one, in a class."
        )


class TestNotes:
    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_entry_is_filled_in(self, source, n):
        text = source("NOTES.md")
        parts = text.split(f"## broken_{n}.py")
        assert len(parts) > 1, f"NOTES.md is missing the broken_{n}.py section."
        body = parts[1].split("\n## ")[0]
        assert PLACEHOLDER not in body, (
            f"The broken_{n}.py entry still has '{PLACEHOLDER}' placeholders."
        )
        assert len(body.split()) >= 40, (
            f"The broken_{n}.py entry is too short. Answer all four prompts."
        )

"""Test harness for the course.

Week 1-2 students write *scripts*, not functions - they have not met `def` yet.
So the grader runs each script as a real program, types answers into it, and
reads what it prints. That grades exactly the thing a beginner actually writes.

Students never need to read this file. Instructors do, when adding a week.

    def test_something(run):
        r = run("hello.py")                       # no input
        r = run("greet.py", answers=["Sam"])      # types "Sam" + Enter
        assert r.lines[0] == "Hello, Sam!"
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest


class Result:
    """What a student's script did when we ran it."""

    def __init__(self, script, stdout, stderr, code):
        self.script = script
        self.stdout = stdout
        self.stderr = stderr
        self.code = code

    @property
    def lines(self):
        """Printed lines, trailing whitespace and blank edges removed."""
        return [ln.rstrip() for ln in self.stdout.strip().splitlines()]

    @property
    def text(self):
        return self.stdout

    def line(self, i):
        """Line i, with a readable failure if the script printed too little."""
        if i >= len(self.lines):
            pytest.fail(
                f"{self.script} printed {len(self.lines)} line(s), "
                f"but the test needed at least {i + 1}.\n"
                f"What it printed:\n{self._shown()}"
            )
        return self.lines[i]

    def require_output(self):
        """Guard for 'you must not do X' tests.

        A check like "do not hard-code the answer" is trivially true of a file
        with nothing in it. Call this first so the check only applies once the
        program actually runs and prints.
        """
        if not self.stdout.strip():
            pytest.fail(
                f"{self.script} has not printed anything yet.\n"
                "Get the output right first - this test checks HOW you did it, "
                "and there is nothing to check yet."
            )
        return self

    def expect(self, text):
        """Assert the program printed this exact text somewhere in its output.

        Used instead of line indexes for any script that calls input(): the
        prompt text lands in stdout too, glued to whatever prints next, so
        line numbers are not reliable. Substring matching is.
        """
        if text not in self.stdout:
            pytest.fail(
                f"\n{self.script} never printed:\n"
                f"  {text}\n\n"
                f"Everything it printed:\n{self._shown()}\n\n"
                "Check spelling, capitals, spaces, and the number of decimal places.\n"
                "(The input() prompts appear in here too - that is normal.)"
            )
        return self

    def _shown(self):
        if not self.stdout.strip():
            return "  (nothing at all)"
        return "\n".join(f"  | {ln}" for ln in self.stdout.rstrip().splitlines())

    def __repr__(self):
        return f"<{self.script} exit={self.code}>"


def _fail_with_traceback(script, answers, res):
    typed = ", ".join(repr(a) for a in answers) if answers else "nothing"
    pytest.fail(
        f"\n{script} crashed instead of finishing.\n"
        f"We typed: {typed}\n\n"
        f"Python said:\n"
        + "\n".join(f"  {ln}" for ln in res.stderr.rstrip().splitlines())
        + "\n\nRead that from the BOTTOM up. The last line is what went wrong;\n"
          "the line above it tells you where.\n"
    )


@pytest.fixture
def run(request):
    """Run a student script that lives next to the test file."""
    script_dir = Path(request.fspath).parent

    def _run(script_name, answers=None, timeout=15, allow_crash=False, env=None):
        path = script_dir / script_name
        if not path.exists():
            pytest.fail(
                f"{script_name} does not exist yet in {script_dir.name}/.\n"
                f"Create it, then run the tests again."
            )

        stdin = ""
        if answers:
            stdin = "".join(f"{a}\n" for a in answers)

        environment = None
        if env:
            environment = {**os.environ, **{k: str(v) for k, v in env.items()}}

        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(script_dir),
                env=environment,
            )
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"\n{script_name} was still running after {timeout} seconds.\n"
                f"Usually this means it is waiting for input you did not give it,\n"
                f"or it asks for input in a different order than the task specified.\n"
            )

        res = Result(script_name, proc.stdout, proc.stderr, proc.returncode)
        if proc.returncode != 0 and not allow_crash:
            _fail_with_traceback(script_name, answers, res)
        return res

    return _run


@pytest.fixture
def source(request):
    """Read the text of a student script that lives next to the test file.

    Use sparingly - grade behaviour, not spelling. Only reach for this when the
    task genuinely constrains *how* something is written (e.g. "use exactly
    three print calls", "do not hard-code the answer").
    """
    script_dir = Path(request.fspath).parent

    def _source(script_name, code_only=False):
        path = script_dir / script_name
        if not path.exists():
            pytest.fail(
                f"{script_name} does not exist yet in {script_dir.name}/.\n"
                f"Create it, then run the tests again."
            )
        text = path.read_text()
        if code_only:
            text = _strip_comments(text)
        return text

    return _source


def _strip_comments(text):
    """Return the source with comments and docstrings removed.

    Stub files describe the task in comments AND in module docstrings, so a
    naive substring check on the raw text passes before the student has written
    anything - the instructions themselves contain the words being looked for.
    Both have to go.

    Line numbers and indentation are preserved (docstring lines are blanked
    rather than deleted), so error messages still point at the right place.
    Falls back to the raw text if the file does not parse - which is exactly
    the case for the deliberately broken files on debugging days.
    """
    import ast
    import io
    import tokenize

    try:
        tree = ast.parse(text)
    except SyntaxError:
        pass
    else:
        blank = set()
        holders = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        for node in ast.walk(tree):
            if not isinstance(node, holders):
                continue
            body = getattr(node, "body", None)
            if not body:
                continue
            first = body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                blank.update(range(first.lineno, (first.end_lineno or first.lineno) + 1))
        if blank:
            lines = text.splitlines(keepends=True)
            for number in blank:
                if 1 <= number <= len(lines):
                    lines[number - 1] = "\n"
            text = "".join(lines)

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return text
    kept = [t for t in tokens if t.type != tokenize.COMMENT]
    try:
        return tokenize.untokenize(kept)
    except Exception:
        return text


@pytest.fixture
def run_variant(request):
    """Run a student script with parts of its source swapped out.

    The automated version of the Friday 'mutate' phase: prove the program
    computes its answers instead of containing them. Swap the data block for a
    different one and the output must follow.

        r = run_variant("ranking.py", {"scores = [340, 892]": "scores = [1, 2]"})

    Every key must appear in the file, or the test fails with a clear message
    rather than silently passing.
    """
    script_dir = Path(request.fspath).parent

    def _run(script_name, replacements, answers=None, timeout=15):
        path = script_dir / script_name
        if not path.exists():
            pytest.fail(f"{script_name} does not exist yet in {script_dir.name}/.")

        text = path.read_text()
        for old, new in replacements.items():
            if old not in text:
                pytest.fail(
                    f"\nThis test swaps the data in {script_name} for a different "
                    f"set, to check your program works it out rather than having "
                    f"it typed in.\n\nTo do that it needs this line, unchanged:\n"
                    f"  {old}\n\n"
                    f"Leave the data block exactly as it was given to you and put "
                    f"your code underneath it."
                )
            text = text.replace(old, new)

        variant = script_dir / f"_variant_{script_name}"
        stdin = "".join(f"{a}\n" for a in answers) if answers else ""
        try:
            variant.write_text(text)
            proc = subprocess.run(
                [sys.executable, str(variant)],
                input=stdin, capture_output=True, text=True,
                timeout=timeout, cwd=str(script_dir),
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"{script_name} did not finish with the swapped data.")
        finally:
            variant.unlink(missing_ok=True)

        res = Result(script_name, proc.stdout, proc.stderr, proc.returncode)
        if proc.returncode != 0:
            _fail_with_traceback(f"{script_name} (with different data)", answers, res)
        return res

    return _run


class Module:
    """A student's module, with friendly errors for things they have not written."""

    def __init__(self, name, module):
        self._name = name
        self._module = module

    def __getattr__(self, attr):
        if not hasattr(self._module, attr):
            defined = [
                n for n in dir(self._module)
                if not n.startswith("_") and callable(getattr(self._module, n))
            ]
            pytest.fail(
                f"\n{self._name} does not define {attr}() yet.\n"
                + (f"What it does define: {', '.join(defined)}\n"
                   if defined else "It defines no functions or classes yet.\n")
                + "Check the spelling in the task - the tests call it by that "
                  "exact name."
            )
        return getattr(self._module, attr)

    def __repr__(self):
        return f"<module {self._name}>"


@pytest.fixture
def load(request):
    """Import a student module that lives next to the test file.

    From Week 3 on, students write functions rather than top-to-bottom scripts,
    so the tests call those functions directly instead of running the file and
    reading its output.

        money = load("money.py")
        assert money.add_tax(100) == 108.00

    Modules are registered under their plain name for the duration of one test,
    so a file that imports a sibling gets the SAME module object this fixture
    returns. Without that, `isinstance(x, Expense)` inside ledger.py would be
    comparing against a different Expense class than the test holds. Everything
    loaded is removed again afterwards, so no test can see another test's state.
    """
    import importlib.util

    script_dir = Path(request.fspath).parent
    before = set(sys.modules)
    loaded = {}

    def _load(script_name):
        path = script_dir / script_name
        if not path.exists():
            pytest.fail(
                f"{script_name} does not exist yet in {script_dir.name}/.\n"
                f"Create it, then run the tests again."
            )

        stem = path.stem
        if stem in loaded:
            return loaded[stem]
        if stem in sys.modules and stem not in before:
            # a sibling already imported it - use that exact object
            module = sys.modules[stem]
            loaded[stem] = Module(script_name, module)
            return loaded[stem]

        spec = importlib.util.spec_from_file_location(stem, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[stem] = module

        old_cwd = os.getcwd()
        old_path = list(sys.path)
        sys.path.insert(0, str(script_dir))
        os.chdir(script_dir)
        try:
            spec.loader.exec_module(module)
        except EOFError:
            pytest.fail(
                f"\n{script_name} asked for input while it was being imported.\n\n"
                "This file should only DEFINE functions and classes. Anything "
                "that runs when the file is imported - an input(), a print(), a "
                "loop - belongs either in a different file or behind:\n\n"
                '    if __name__ == "__main__":\n'
            )
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            sys.modules.pop(stem, None)
            pytest.fail(
                f"\n{script_name} crashed while being imported "
                f"({type(exc).__name__}).\n\n"
                + "\n".join(f"  {ln}" for ln in tb.rstrip().splitlines()[-8:])
                + "\n\nEverything in the file runs top to bottom when it is "
                  "imported. Fix that error before the tests can call anything."
            )
        finally:
            os.chdir(old_cwd)
            sys.path[:] = old_path

        loaded[stem] = Module(script_name, module)
        return loaded[stem]

    yield _load

    # Only evict the student's own modules. Popping third-party packages here
    # would make the next test re-import them, and a library imported twice has
    # two of every class - which breaks isinstance checks deep inside it.
    root = str(script_dir)
    for name in set(sys.modules) - before:
        module = sys.modules.get(name)
        origin = getattr(module, "__file__", None) or ""
        if origin.startswith(root):
            sys.modules.pop(name, None)


@pytest.fixture
def run_student_tests(request):
    """Run a test file the STUDENT wrote, against a module we control.

    Used in Week 4, where the exercise is writing tests rather than passing
    them. Their suite is run against a deliberately broken version of the
    module; a suite that still passes has not tested anything.

        result = run_student_tests("test_shapes.py", "shapes.py",
                                   {"return self.width * self.height":
                                    "return self.width + self.height"})
        assert not result.passed

    Everything happens in a temp directory, so nothing is modified in place.
    """
    import shutil
    import tempfile

    script_dir = Path(request.fspath).parent

    class Outcome:
        def __init__(self, passed, output, code=0):
            self.passed = passed
            self.output = output
            self.code = code

        @property
        def no_tests(self):
            """pytest exits 5 when it collected nothing at all."""
            return self.code == 5

    def _run(test_file, module_file, mutations=None, timeout=60):
        test_path = script_dir / test_file
        module_path = script_dir / module_file
        for p in (test_path, module_path):
            if not p.exists():
                pytest.fail(f"{p.name} does not exist yet in {script_dir.name}/.")

        source_text = module_path.read_text()
        for old, new in (mutations or {}).items():
            if old not in source_text:
                pytest.fail(
                    f"Internal: mutation target not found in {module_file}:\n  {old}"
                )
            source_text = source_text.replace(old, new)

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            shutil.copy2(test_path, tmp / test_file)
            (tmp / module_file).write_text(source_text)
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", test_file,
                 "-q", "--tb=short", "-p", "no:cacheprovider"],
                cwd=str(tmp), capture_output=True, text=True, timeout=timeout,
            )
        return Outcome(proc.returncode == 0, proc.stdout + proc.stderr,
                       proc.returncode)

    return _run


@pytest.fixture
def run_tests_against(request):
    """Run a student's test file against modules whose source WE supply.

    Like run_student_tests, but the modules are given as text rather than read
    from the student's folder. Used to check a test suite against deliberately
    hollow implementations without shipping a working one they could copy.

        result = run_tests_against("test_ledger.py", {"ledger.py": HOLLOW})
        assert not result.passed
    """
    import shutil
    import tempfile

    script_dir = Path(request.fspath).parent

    class Outcome:
        def __init__(self, passed, output, code=0):
            self.passed = passed
            self.output = output
            self.code = code

        @property
        def no_tests(self):
            """pytest exits 5 when it collected nothing at all."""
            return self.code == 5

    def _run(test_file, files, also_copy=(), timeout=60):
        test_path = script_dir / test_file
        if not test_path.exists():
            pytest.fail(f"{test_file} does not exist yet in {script_dir.name}/.")

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            shutil.copy2(test_path, tmp / test_file)
            for name in also_copy:
                if (script_dir / name).exists():
                    shutil.copy2(script_dir / name, tmp / name)
            for name, text in files.items():
                (tmp / name).write_text(text)
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", test_file,
                 "-q", "--tb=line", "-p", "no:cacheprovider"],
                cwd=str(tmp), capture_output=True, text=True, timeout=timeout,
            )
        return Outcome(proc.returncode == 0, proc.stdout + proc.stderr,
                       proc.returncode)

    return _run

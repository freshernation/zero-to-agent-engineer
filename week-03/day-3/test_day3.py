"""Week 3, Day 3 - files, JSON, modules.

Run me:  pytest week-03/day-3 -v

`tmp_path` is a pytest fixture giving each test its own empty folder, so nothing
you write here ends up in your repo.
"""

import json
import pytest


@pytest.fixture(autouse=True)
def clean_visits(request):
    """app.py writes visits.json next to itself. Remove it around every test."""
    from pathlib import Path
    visits = Path(request.fspath).parent / "visits.json"
    visits.unlink(missing_ok=True)
    yield
    visits.unlink(missing_ok=True)


class TestNotes:
    def test_save_then_load(self, load, tmp_path):
        notes = load("notes.py")
        path = str(tmp_path / "a.txt")
        notes.save_lines(path, ["one", "two", "three"])
        assert notes.load_lines(path) == ["one", "two", "three"]

    def test_load_strips_newlines(self, load, tmp_path):
        notes = load("notes.py")
        path = tmp_path / "a.txt"
        path.write_text("one\ntwo\n")
        result = notes.load_lines(str(path))
        assert result == ["one", "two"], (
            f"Got {result}. readlines() leaves the \\n on the end of each line - "
            "strip it off before you hand the list back."
        )

    def test_load_missing_file(self, load, tmp_path):
        notes = load("notes.py")
        assert notes.load_lines(str(tmp_path / "nothing.txt")) == []

    def test_save_replaces(self, load, tmp_path):
        notes = load("notes.py")
        path = str(tmp_path / "a.txt")
        notes.save_lines(path, ["old", "stuff", "here"])
        notes.save_lines(path, ["new"])
        assert notes.load_lines(path) == ["new"]

    def test_append_keeps_what_was_there(self, load, tmp_path):
        notes = load("notes.py")
        path = str(tmp_path / "a.txt")
        notes.save_lines(path, ["one", "two"])
        notes.append_line(path, "three")
        assert notes.load_lines(path) == ["one", "two", "three"], (
            "append_line wiped the file. Opening with mode 'w' empties it - "
            "you want 'a'."
        )

    def test_append_to_a_new_file(self, load, tmp_path):
        notes = load("notes.py")
        path = str(tmp_path / "fresh.txt")
        notes.append_line(path, "first")
        assert notes.load_lines(path) == ["first"]


class TestStore:
    def test_save_then_load_a_dict(self, load, tmp_path):
        store = load("store.py")
        path = str(tmp_path / "d.json")
        store.save_data(path, {"a": 1, "b": [1, 2, 3]})
        assert store.load_data(path) == {"a": 1, "b": [1, 2, 3]}

    def test_save_then_load_a_list_of_dicts(self, load, tmp_path):
        store = load("store.py")
        path = str(tmp_path / "d.json")
        data = [{"item": "Coffee", "amount": 4.5}, {"item": "Bus", "amount": 2.0}]
        store.save_data(path, data)
        assert store.load_data(path) == data

    def test_writes_real_json(self, load, tmp_path):
        store = load("store.py")
        path = tmp_path / "d.json"
        store.save_data(str(path), {"a": 1})
        assert json.loads(path.read_text()) == {"a": 1}, (
            "The file should contain valid JSON. Use json.dump, not str() or write()."
        )

    def test_missing_file_returns_default(self, load, tmp_path):
        store = load("store.py")
        missing = str(tmp_path / "nope.json")
        assert store.load_data(missing) is None
        assert store.load_data(missing, []) == []
        assert store.load_data(missing, default={}) == {}

    def test_damaged_file_returns_default(self, load, tmp_path):
        """The case that works fine until the day it does not."""
        store = load("store.py")
        path = tmp_path / "broken.json"
        path.write_text("{not json at all")
        assert store.load_data(str(path), []) == [], (
            "A file that exists but contains damaged JSON raises "
            "json.JSONDecodeError, not FileNotFoundError. Catch both."
        )

    def test_empty_file_returns_default(self, load, tmp_path):
        store = load("store.py")
        path = tmp_path / "empty.json"
        path.write_text("")
        assert store.load_data(str(path), []) == []


class TestApp:
    def test_importing_it_prints_nothing(self, load, capsys):
        app = load("app.py")
        printed = capsys.readouterr().out
        app.record_visit  # nothing to check until it exists
        assert printed == "", (
            f"Importing app.py printed {printed!r}.\n"
            'Put the printing behind:  if __name__ == "__main__":\n'
            "Everything in a file runs when it is imported - that is what the "
            "guard is for."
        )

    def test_record_visit_returns_the_count(self, load, tmp_path):
        app = load("app.py")
        path = str(tmp_path / "v.json")
        assert app.record_visit(path) == 1
        assert app.record_visit(path) == 2
        assert app.record_visit(path) == 3

    def test_record_visit_persists(self, load, tmp_path):
        """A fresh import must still see the saved count."""
        path = str(tmp_path / "v.json")
        load("app.py").record_visit(path)
        load("app.py").record_visit(path)
        assert load("app.py").record_visit(path) == 3

    def test_running_it_prints(self, run):
        run("app.py").expect("Visits: 1")

    def test_running_it_twice_counts_up(self, run):
        run("app.py").expect("Visits: 1")
        run("app.py").expect("Visits: 2")

    def test_uses_store(self, source):
        code = source("app.py", code_only=True)
        assert "store" in code, (
            "app.py should use store.py rather than doing its own JSON handling. "
            "That is the point of splitting them."
        )

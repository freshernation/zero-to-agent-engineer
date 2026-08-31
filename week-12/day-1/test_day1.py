"""Week 12, Day 1 - the artifacts.

Run me:  pytest week-12/day-1 -v

These tests check that the words are there. Whether they are any good is what
Friday is for - and what an interviewer decides in ninety seconds.
"""

import re

import pytest

BEATS = ("one_line", "decision", "alternative", "broke", "next_step")


class TestProjects:
    def test_three_of_them(self, load):
        assert len(load("story.py").PROJECTS) == 3

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_every_field_is_present(self, load, index):
        project = load("story.py").PROJECTS[index]
        assert project["name"]
        for field in BEATS:
            assert project.get(field), f"{project['name']} has no {field}."

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_the_one_liner_has_a_number(self, load, index):
        project = load("story.py").PROJECTS[index]
        assert re.search(r"\d", project["one_line"]), (
            f"'{project['one_line']}' has no number in it. A line with a figure "
            "in it could only have been written by somebody who built the thing."
        )

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_the_broke_beat_is_specific(self, load, index):
        project = load("story.py").PROJECTS[index]
        assert len(project["broke"].split()) >= 10, (
            "The 'what went wrong' beat is the one that lands, and it is the one "
            "people skip. Name the actual error or symptom."
        )

    def test_projects_are_different(self, load):
        names = [p["name"] for p in load("story.py").PROJECTS]
        assert len(set(names)) == 3


class TestOneLiner:
    def test_returns_a_string(self, load):
        mod = load("story.py")
        line = mod.one_liner(mod.PROJECTS[0])
        assert isinstance(line, str) and len(line.split()) >= 8

    def test_mentions_the_project(self, load):
        mod = load("story.py")
        project = mod.PROJECTS[0]
        assert project["name"] in mod.one_liner(project)


class TestStory:
    def test_four_beats(self, load):
        mod = load("story.py")
        told = mod.story(mod.PROJECTS[0])
        assert told.count("\n") >= 3, "Four beats, one per line at least."

    def test_the_beats_are_in_order(self, load):
        mod = load("story.py")
        project = mod.PROJECTS[0]
        told = mod.story(project)
        positions = [told.find(project[beat][:20]) for beat in
                     ("one_line", "decision", "broke", "next_step")]
        assert all(p >= 0 for p in positions), "A beat is missing from the story."
        assert positions == sorted(positions), (
            "The beats are out of order. What it does, the decision, what broke, "
            "what next - the order is the whole structure."
        )


class TestCheck:
    def test_a_good_project_passes(self, load):
        mod = load("story.py")
        for project in mod.PROJECTS:
            result = mod.check(project)
            assert result["ok"] is True, (
                f"{project['name']}: {result['problems']}"
            )

    def test_catches_a_missing_number(self, load):
        mod = load("story.py")
        bad = {**mod.PROJECTS[0], "one_line": "built an agent with python and langchain"}
        result = mod.check(bad)
        assert result["ok"] is False
        assert any("number" in p.lower() for p in result["problems"])

    def test_catches_a_thin_beat(self, load):
        mod = load("story.py")
        bad = {**mod.PROJECTS[0], "decision": "used langgraph"}
        assert mod.check(bad)["ok"] is False

    def test_catches_a_vague_failure(self, load):
        mod = load("story.py")
        bad = {**mod.PROJECTS[0], "broke": "some bugs"}
        assert mod.check(bad)["ok"] is False


class TestResume:
    HEADINGS = ["Projects", "Skills", "Experience", "Education"]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_has_the_section(self, source, heading):
        text = source("RESUME.md")
        assert f"## {heading}" in text, f"RESUME.md has no '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert body.strip(), f"The '{heading}' section is empty."

    def test_projects_come_first(self, source):
        text = re.sub(r"<!--.*?-->", "", source("RESUME.md"), flags=re.S)
        assert "[Your name]" not in text, "Write the résumé first."
        positions = {h: text.find(f"## {h}") for h in self.HEADINGS}
        assert positions["Projects"] == min(positions.values()), (
            "Projects are not the first section. For a career changer they are "
            "the evidence and everything else is context - this is the single "
            "most important formatting decision on the page."
        )

    def test_projects_section_has_three_lines_with_numbers(self, source):
        section = source("RESUME.md").split("## Projects", 1)[1].split("\n## ")[0]
        lines = [ln for ln in section.splitlines() if ln.strip().startswith(("-", "*"))]
        assert len(lines) >= 3, f"Found {len(lines)} project lines, expected 3."
        with_numbers = [ln for ln in lines if re.search(r"\d", ln)]
        assert len(with_numbers) >= 3, (
            "Every project line needs a number in it."
        )

    def test_is_written(self, source):
        text = source("RESUME.md")
        body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        assert "[Your name]" not in body, "Put your actual name at the top."
        assert len(body.split()) >= 120


class TestGithubAudit:
    def test_covers_three_projects(self, source):
        text = re.sub(r"<!--.*?-->", "", source("GITHUB.md"), flags=re.S)
        assert text.count("## Project") >= 3
        filled = [
            line for line in text.splitlines()
            if "Repository:" in line and line.split("Repository:", 1)[1].strip()
        ]
        assert len(filled) >= 3, "Fill in the repository for each project."

    def test_is_filled_in(self, source):
        text = re.sub(r"<!--.*?-->", "", source("GITHUB.md"), flags=re.S)
        for label in ("Repository:", "Pinned:", "Live link:"):
            filled = [
                line for line in text.splitlines()
                if label in line and line.split(label, 1)[1].strip()
            ]
            assert len(filled) >= 3, (
                f"'{label}' is blank for at least one project. Check it for real "
                "rather than from memory - that is the whole exercise."
            )

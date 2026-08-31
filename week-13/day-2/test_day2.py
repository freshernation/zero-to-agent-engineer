"""Week 13, Day 2 - applications.

Run me:  pytest week-13/day-2 -v
"""

import re

import pytest

SOURCES = {"referral", "direct", "board", "agency"}
STATUSES = {"applied", "screening", "interview", "offer", "rejected", "ghosted"}

SAMPLE = [
    {"company": "Alpha", "role": "AI Engineer", "source": "referral",
     "applied": "2026-01-05", "status": "interview"},
    {"company": "Beta", "role": "Backend", "source": "board",
     "applied": "2026-01-05", "status": "applied"},
    {"company": "Gamma", "role": "Solutions", "source": "board",
     "applied": "2026-01-06", "status": "rejected"},
    {"company": "Delta", "role": "Automation", "source": "direct",
     "applied": "2026-01-20", "status": "applied"},
]


class TestTheList:
    def test_at_least_ten(self, load):
        assert len(load("applications.py").APPLICATIONS) >= 10, (
            "Ten good applications beat two perfect ones, for the same reason "
            "the tenth mock was better than the first."
        )

    def test_every_field(self, load):
        for app in load("applications.py").APPLICATIONS:
            for field in ("company", "role", "source", "applied", "status"):
                assert app.get(field), f"{app.get('company')} has no {field}."

    def test_sources_are_known(self, load):
        for app in load("applications.py").APPLICATIONS:
            assert app["source"] in SOURCES, f"Unknown source {app['source']!r}."

    def test_statuses_are_known(self, load):
        for app in load("applications.py").APPLICATIONS:
            assert app["status"] in STATUSES, f"Unknown status {app['status']!r}."

    def test_dates_are_iso(self, load):
        for app in load("applications.py").APPLICATIONS:
            assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", app["applied"]), (
                f"{app['company']}'s date is {app['applied']!r} - use YYYY-MM-DD."
            )

    def test_more_than_one_channel(self, load):
        sources = {a["source"] for a in load("applications.py").APPLICATIONS}
        assert len(sources) >= 2, (
            "Every application went through one channel. Most people spend all "
            "their effort on the one that converts worst, because it is the one "
            "that does not involve talking to anybody."
        )


class TestCounts:
    def test_count_by_status(self, load):
        counts = load("applications.py").count_by_status(SAMPLE)
        assert counts["applied"] == 2
        assert counts["interview"] == 1
        assert counts["rejected"] == 1

    def test_count_by_status_of_nothing(self, load):
        assert load("applications.py").count_by_status([]) == {}

    def test_by_source(self, load):
        assert load("applications.py").by_source(SAMPLE) == {
            "referral": 1, "board": 2, "direct": 1,
        }


class TestResponseRate:
    def test_rate(self, load):
        """Alpha interviewing and Gamma rejected both count as responses."""
        assert load("applications.py").response_rate(SAMPLE) == 0.5

    def test_ghosted_does_not_count_as_a_response(self, load):
        apps = SAMPLE + [{
            "company": "Epsilon", "role": "x", "source": "board",
            "applied": "2026-01-01", "status": "ghosted",
        }]
        assert load("applications.py").response_rate(apps) == 0.4

    def test_rate_of_nothing(self, load):
        assert load("applications.py").response_rate([]) == 0.0

    def test_rate_by_source(self, load):
        rates = load("applications.py").response_rate_by_source(SAMPLE)
        assert rates["referral"] == 1.0
        assert rates["board"] == 0.5
        assert rates["direct"] == 0.0

    def test_best_source(self, load):
        assert load("applications.py").best_source(SAMPLE) == "referral"

    def test_best_source_ties_alphabetically(self, load):
        apps = [
            {"company": "A", "role": "x", "source": "referral",
             "applied": "2026-01-01", "status": "interview"},
            {"company": "B", "role": "x", "source": "direct",
             "applied": "2026-01-01", "status": "interview"},
        ]
        assert load("applications.py").best_source(apps) == "direct"

    def test_best_source_of_nothing(self, load):
        assert load("applications.py").best_source([]) is None


class TestFollowUp:
    def test_finds_the_stale_ones(self, load):
        stale = load("applications.py").needs_follow_up(SAMPLE, "2026-01-26")
        assert "Beta" in stale, (
            "Beta was applied on the 5th and is still 'applied' three weeks later."
        )

    def test_ignores_recent_ones(self, load):
        stale = load("applications.py").needs_follow_up(SAMPLE, "2026-01-26")
        assert "Delta" not in stale, (
            "Delta went out on the 20th - four working days ago. Too soon."
        )

    def test_ignores_ones_that_moved(self, load):
        stale = load("applications.py").needs_follow_up(SAMPLE, "2026-01-26")
        assert "Alpha" not in stale and "Gamma" not in stale

    def test_counts_working_days(self, load):
        """The 5th to the 19th is ten working days, not fourteen."""
        apps = [{"company": "Beta", "role": "x", "source": "board",
                 "applied": "2026-01-05", "status": "applied"}]
        mod = load("applications.py")
        assert mod.needs_follow_up(apps, "2026-01-19") == ["Beta"]
        assert mod.needs_follow_up(apps, "2026-01-16") == []

    def test_custom_window(self, load):
        apps = [{"company": "Beta", "role": "x", "source": "board",
                 "applied": "2026-01-05", "status": "applied"}]
        assert load("applications.py").needs_follow_up(
            apps, "2026-01-08", days=3
        ) == ["Beta"]


class TestDocument:
    def test_has_a_table(self, source):
        text = re.sub(r"<!--.*?-->", "", source("APPLICATIONS.md"), flags=re.S)
        rows = [
            line for line in text.splitlines()
            if line.strip().startswith("|") and "---" not in line
            and "Company" not in line and line.split("|")[1].strip()
        ]
        assert len(rows) >= 10, f"{len(rows)} rows filled in, expected 10."

    def test_what_i_am_learning(self, source):
        text = source("APPLICATIONS.md")
        assert "## What I am learning" in text
        section = text.split("## What I am learning", 1)[1]
        assert len(section.split()) >= 100, (
            "The numbers only teach you something if you write down what they "
            "say. Which channel is working, and what are you going to do about it?"
        )

    def test_instructions_removed(self, source):
        assert "<!--" not in source("APPLICATIONS.md")

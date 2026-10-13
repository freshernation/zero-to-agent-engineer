"""Week 11, Day 2 - the handoff.

Run me:  pytest week-11/day-2 -v
"""

import pytest

BRIEF = (
    "Goal: Find the population of Lisbon.\n"
    "\n"
    "What is known:\n"
    "- The user wants a total for two cities\n"
    "- Lagos is already done: 15400000\n"
    "\n"
    "Return: The number, digits only."
)


class TestBuildBrief:
    def test_the_three_parts(self, load):
        brief = load("brief.py").build_brief(
            "Find the population of Lisbon.",
            ["The user wants a total for two cities", "Lagos is already done: 15400000"],
            "The number, digits only.",
        )
        assert brief == BRIEF

    def test_nothing_known(self, load):
        brief = load("brief.py").build_brief("Find X.", [], "One line.")
        assert brief == "Goal: Find X.\n\nWhat is known:\n- nothing yet\n\nReturn: One line."

    @pytest.mark.parametrize("goal,returns", [("", "x"), ("   ", "x"), ("x", ""), ("x", " ")])
    def test_a_brief_without_a_goal_or_a_return_is_refused(self, load, goal, returns):
        with pytest.raises(ValueError):
            load("brief.py").build_brief(goal, [], returns)

    def test_a_built_brief_is_complete(self, load):
        mod = load("brief.py")
        assert mod.missing_parts(mod.build_brief("g", ["k"], "r")) == []


class TestMissingParts:
    def test_a_one_line_brief_is_missing_two(self, load):
        assert load("brief.py").missing_parts("Goal: find the population") == [
            "What is known", "Return"
        ], (
            "This is what a model writes when nobody tells it otherwise: the "
            "goal, and nothing the worker would need to do it well."
        )

    def test_a_bare_sentence_is_missing_all_three(self, load):
        assert load("brief.py").missing_parts("look up Lisbon please") == [
            "Goal", "What is known", "Return"
        ]

    def test_capitals_do_not_matter(self, load):
        text = "GOAL: x\nwhat is known:\n- y\nreturn: z"
        assert load("brief.py").missing_parts(text) == []

    def test_the_label_has_to_start_a_line(self, load):
        text = "Please note the Goal: is unclear.\nWhat is known:\n- y\nReturn: z"
        assert load("brief.py").missing_parts(text) == ["Goal"]

    def test_indented_labels_count(self, load):
        assert load("brief.py").missing_parts("  Goal: x\n  What is known:\n  Return: z") == []


RESULT = {
    "worker": "researcher",
    "text": "Lisbon: 545000.",
    "stopped": "answered",
    "steps": 3,
    "input_tokens": 900,
    "output_tokens": 100,
    "tool_calls": [
        {"name": "lookup_population", "input": {"city": "Lisbon"}, "result": "545000"},
        {"name": "lookup_population", "input": {"city": "Porto"},
         "result": "Tool failed: No data for Porto"},
    ],
}


class TestSizes:
    def test_estimate(self, load):
        mod = load("brief.py")
        assert mod.estimate_tokens("a" * 400) == 100
        assert mod.estimate_tokens("abc") == 0
        assert mod.estimate_tokens("") == 0

    def test_crossed_counts_both_directions(self, load):
        assert load("brief.py").crossed("a" * 400, "b" * 40) == 110

    def test_kept_out(self, load):
        # The worker used 1000 tokens; 10 of them came back.
        assert load("brief.py").kept_out(RESULT, "b" * 40) == 990, (
            "The worker read and wrote 1000 tokens and sent back about 10. The "
            "other 990 never entered the asker's context - that is what a "
            "separate worker buys."
        )

    def test_kept_out_is_never_negative(self, load):
        small = {**RESULT, "input_tokens": 5, "output_tokens": 5}
        assert load("brief.py").kept_out(small, "b" * 400) == 0


class TestLost:
    def test_what_did_not_come_back(self, load):
        assert load("brief.py").lost(RESULT, "Lisbon: 545000.") == [
            "Tool failed: No data for Porto"
        ], (
            "The worker tried Porto, failed, and did not mention it. Whoever "
            "asked will never know - that is what a handoff loses."
        )

    def test_nothing_lost_when_the_report_carries_it(self, load):
        report = "Lisbon: 545000. Tool failed: No data for Porto"
        assert load("brief.py").lost(RESULT, report) == []

    def test_everything_lost_in_a_bare_report(self, load):
        assert load("brief.py").lost(RESULT, "Done.") == [
            "545000", "Tool failed: No data for Porto"
        ]

    def test_no_tool_calls(self, load):
        assert load("brief.py").lost({**RESULT, "tool_calls": []}, "x") == []

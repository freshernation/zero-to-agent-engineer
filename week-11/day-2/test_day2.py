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


class TestBudgetPerWorker:
    def test_report_budget(self, load):
        assert load("brief.py").report_budget(8000, 2000, 3) == 2000

    @pytest.mark.parametrize("window,reserve,workers", [(8000, 2000, 0), (1000, 1000, 2)])
    def test_impossible_budgets(self, load, window, reserve, workers):
        with pytest.raises(ValueError):
            load("brief.py").report_budget(window, reserve, workers)

    def test_a_report_inside_its_budget_is_unchanged(self, load):
        assert load("brief.py").fit_report("Lisbon: 545000.", 10) == "Lisbon: 545000."

    def test_a_long_report_is_cut_and_says_so(self, load):
        fitted = load("brief.py").fit_report("x" * 2000, 100)
        assert fitted == "x" * 400 + " [cut: 1600 characters over this worker's budget]", (
            "A report that is cut without saying so is a fact lost in the handoff "
            "that nobody can see."
        )

    def test_one_verbose_worker_cannot_crowd_out_the_others(self, load):
        brief = load("brief.py")
        share = brief.report_budget(1200, 300, 3)
        reports = [brief.fit_report("y" * 3000, share), brief.fit_report("Lagos: 15400000.", share),
                   brief.fit_report("Bogota: 7900000.", share)]
        assert sum(brief.estimate_tokens(r) for r in reports) <= 1200 - 300 + 20
        assert reports[1] == "Lagos: 15400000."

    def test_over_budget(self, load):
        results = [{**RESULT, "worker": "researcher", "input_tokens": 900},
                   {**RESULT, "worker": "analyst", "input_tokens": 300}]
        assert load("brief.py").over_budget(results, 500) == ["researcher"]
        assert load("brief.py").over_budget(results, 1000) == []

